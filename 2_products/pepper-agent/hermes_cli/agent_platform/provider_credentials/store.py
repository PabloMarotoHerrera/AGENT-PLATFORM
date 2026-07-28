"""Internal dedicated store boundary for governed provider credentials."""

from __future__ import annotations

import ctypes
from ctypes import wintypes
import json
import os
import stat
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import SecretStr

from hermes_cli.agent_platform.provider_credentials.client_tokens import (
    ProviderClientTokenMetadataError,
    derive_openai_codex_client_token_status,
)
from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_HERMES_PROVIDER_ID,
    OPENAI_CODEX_INTERNAL_LABEL,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    PROVIDER_CREDENTIAL_SCHEMA_VERSION,
    OpenAICodexOAuthCredential,
    ProviderClientTokenStatus,
    ProviderCredentialLocalClearResult,
    ProviderCredentialStatus,
)


_AUTH_FILE_NAME = "auth.json"
_MAX_AUTH_STORE_BYTES = 262_144
_FIXED_POOL_SOURCE = "manual:device_code"
_SINGLETON_SOURCE_TO_SUPPRESS = "device_code"
_POSIX_DIRECTORY_MODE = stat.S_IRWXU
_POSIX_FILE_MODE = stat.S_IRUSR | stat.S_IWUSR
_WINDOWS_FORBIDDEN_SIDS = frozenset({
    "S-1-1-0",
    "S-1-5-11",
    "S-1-5-32-545",
})
_WINDOWS_STATIC_ALLOWED_SIDS = frozenset({
    "S-1-5-18",
    "S-1-5-32-544",
})


class ProviderCredentialStoreError(RuntimeError):
    """Base class for bounded credential-store errors."""

    error_code = "provider_credential_store_error"

    def __init__(self, *, validation_category: str, detail: str | None = None) -> None:
        self.validation_category = _safe_text(validation_category)
        self.detail = _safe_text(detail) if detail else None
        fragments = [
            f"code={self.error_code}",
            f"validation_category={self.validation_category}",
        ]
        if self.detail:
            fragments.append(f"detail={self.detail}")
        super().__init__(" ".join(fragments))


class InvalidProviderCredentialStoreRootError(ProviderCredentialStoreError):
    error_code = "invalid_provider_credential_store_root"


class InvalidProviderCredentialStoreError(ProviderCredentialStoreError):
    error_code = "invalid_provider_credential_store"


class ExistingProviderCredentialStoreError(ProviderCredentialStoreError):
    error_code = "existing_provider_credential_store"


class MissingProviderCredentialError(ProviderCredentialStoreError):
    error_code = "missing_provider_credential"


class ProviderCredentialStoreProtectionError(ProviderCredentialStoreError):
    error_code = "provider_credential_store_protection_error"


class ProviderCredentialStoreWriteError(ProviderCredentialStoreError):
    error_code = "provider_credential_store_write_error"


@dataclass(frozen=True, slots=True)
class StoreProtectionReport:
    """Secret-free protection evidence for a store path role."""

    path_role: str
    platform: str
    protected: bool
    dacl_inspected: bool = False
    allowed_principal_count: int = 0


class StoreProtectionBackend:
    """Production protection backend with fail-closed Windows DACL validation."""

    def prepare_directory(self, path: Path) -> StoreProtectionReport:
        _reject_redirect(path, path_role="store_directory")
        path.mkdir(mode=_POSIX_DIRECTORY_MODE, parents=True, exist_ok=True)
        if os.name == "nt":
            _apply_windows_dacl(path)
        else:
            path.chmod(_POSIX_DIRECTORY_MODE)
        return self.validate_directory(path)

    def prepare_file(self, path: Path) -> StoreProtectionReport:
        _reject_redirect(path, path_role="auth_file")
        if os.name == "nt":
            _apply_windows_dacl(path)
        else:
            path.chmod(_POSIX_FILE_MODE)
        return self.validate_file(path)

    def validate_directory(self, path: Path) -> StoreProtectionReport:
        _reject_redirect(path, path_role="store_directory")
        if not path.is_dir():
            raise ProviderCredentialStoreProtectionError(
                validation_category="directory_missing"
            )
        if os.name == "nt":
            return _validate_windows_dacl(path, path_role="store_directory")
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode != _POSIX_DIRECTORY_MODE:
            raise ProviderCredentialStoreProtectionError(
                validation_category="posix_directory_mode_not_0700",
                detail=oct(mode),
            )
        return StoreProtectionReport("store_directory", "posix", True)

    def validate_file(self, path: Path) -> StoreProtectionReport:
        _reject_redirect(path, path_role="auth_file")
        if not path.is_file():
            raise ProviderCredentialStoreProtectionError(
                validation_category="auth_file_missing"
            )
        if os.name == "nt":
            return _validate_windows_dacl(path, path_role="auth_file")
        mode = stat.S_IMODE(path.stat().st_mode)
        if mode != _POSIX_FILE_MODE:
            raise ProviderCredentialStoreProtectionError(
                validation_category="posix_file_mode_not_0600",
                detail=oct(mode),
            )
        return StoreProtectionReport("auth_file", "posix", True)


def default_openai_codex_credential_store_root(hermes_home: Path | None = None) -> Path:
    """Return the governed durable store root below the active Hermes home."""

    if hermes_home is None:
        from hermes_constants import get_hermes_home

        hermes_home = get_hermes_home()
    return (
        Path(hermes_home)
        / "agent-platform"
        / "provider-credentials"
        / "agent-platform"
        / "provider-credentials"
        / OPENAI_CODEX_CREDENTIAL_STORE_ID
    )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _format_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_utc(value: Any) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise InvalidProviderCredentialStoreError(
            validation_category="datetime_missing"
        )
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        raise InvalidProviderCredentialStoreError(
            validation_category="datetime_invalid"
        ) from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise InvalidProviderCredentialStoreError(
            validation_category="datetime_not_utc"
        )
    return parsed.astimezone(timezone.utc)


def _safe_text(value: object) -> str:
    return "".join(character for character in str(value) if 32 <= ord(character) < 127)[
        :120
    ]


def _contains_control(value: str) -> bool:
    return any(ord(character) < 32 for character in value)


def _is_reparse_or_symlink(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _reject_redirect(path: Path, *, path_role: str) -> None:
    if path.exists() and _is_reparse_or_symlink(path):
        raise ProviderCredentialStoreProtectionError(
            validation_category="redirect_detected",
            detail=path_role,
        )


def _auth_file_for_root(trusted_store_root: Path) -> Path:
    root = Path(trusted_store_root)
    if _contains_control(str(root)):
        raise InvalidProviderCredentialStoreRootError(
            validation_category="control_character"
        )
    if not root.is_absolute():
        raise InvalidProviderCredentialStoreRootError(
            validation_category="not_absolute"
        )
    try:
        resolved_root = root.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        raise InvalidProviderCredentialStoreRootError(
            validation_category="resolve_failed",
            detail=exc.__class__.__name__,
        ) from None
    if resolved_root == Path(resolved_root.anchor):
        raise InvalidProviderCredentialStoreRootError(
            validation_category="filesystem_root"
        )
    if root.exists() and not root.is_dir():
        raise InvalidProviderCredentialStoreRootError(
            validation_category="not_directory"
        )
    if root.exists() and _is_reparse_or_symlink(root):
        raise InvalidProviderCredentialStoreRootError(validation_category="redirect")
    return resolved_root / _AUTH_FILE_NAME


def _protection_backend(
    backend: StoreProtectionBackend | None,
) -> StoreProtectionBackend:
    return backend if backend is not None else StoreProtectionBackend()


def _load_json_auth_store(auth_file: Path) -> dict[str, Any]:
    if not auth_file.exists():
        raise MissingProviderCredentialError(validation_category="auth_store_missing")
    try:
        if auth_file.stat().st_size > _MAX_AUTH_STORE_BYTES:
            raise InvalidProviderCredentialStoreError(
                validation_category="auth_store_too_large"
            )
        raw = json.loads(auth_file.read_text(encoding="utf-8"))
    except ProviderCredentialStoreError:
        raise
    except Exception as exc:
        raise InvalidProviderCredentialStoreError(
            validation_category="auth_store_unreadable",
            detail=exc.__class__.__name__,
        ) from None
    if not isinstance(raw, dict):
        raise InvalidProviderCredentialStoreError(
            validation_category="auth_store_not_object"
        )
    return raw


def _require_dict(value: Any, category: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InvalidProviderCredentialStoreError(validation_category=category)
    return value


def _require_token(value: Any, category: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidProviderCredentialStoreError(validation_category=category)
    if len(value) > 16_384 or any(ord(character) < 32 for character in value):
        raise InvalidProviderCredentialStoreError(
            validation_category=f"{category}_invalid"
        )
    return value.strip()


def validate_windows_dacl_principals(
    principal_sids: set[str], *, current_user_sid: str
) -> StoreProtectionReport:
    """Validate parsed Windows allow-ACE SIDs against the governed policy."""

    if not principal_sids:
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_dacl_empty"
        )
    if not current_user_sid:
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_current_user_unknown"
        )
    forbidden = principal_sids & _WINDOWS_FORBIDDEN_SIDS
    if forbidden:
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_forbidden_principal",
            detail=sorted(forbidden)[0],
        )
    allowed = set(_WINDOWS_STATIC_ALLOWED_SIDS)
    allowed.add(current_user_sid)
    unexpected = principal_sids - allowed
    if unexpected:
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_unexpected_principal",
            detail=sorted(unexpected)[0],
        )
    if current_user_sid not in principal_sids:
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_user_missing"
        )
    return StoreProtectionReport(
        "windows_dacl",
        "windows",
        True,
        dacl_inspected=True,
        allowed_principal_count=len(principal_sids),
    )


def _validate_windows_dacl(path: Path, *, path_role: str) -> StoreProtectionReport:
    if os.name != "nt":
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_dacl_on_posix"
        )
    try:
        principal_sids = _read_windows_allowed_dacl_sids(path)
        current_user_sid = _current_windows_user_sid()
        validate_windows_dacl_principals(
            principal_sids,
            current_user_sid=current_user_sid,
        )
    except ProviderCredentialStoreError:
        raise
    except Exception as exc:
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_dacl_inspection_failed",
            detail=exc.__class__.__name__,
        ) from None
    return StoreProtectionReport(
        path_role,
        "windows",
        True,
        dacl_inspected=True,
        allowed_principal_count=len(principal_sids),
    )


def _set_ctypes_signature(
    function: Any, *, argtypes: tuple[Any, ...], restype: Any
) -> None:
    try:
        function.argtypes = argtypes
        function.restype = restype
    except AttributeError:
        return


def _windows_security_libraries() -> tuple[Any, Any]:
    advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    lpvoid_pointer = ctypes.POINTER(wintypes.LPVOID)
    _set_ctypes_signature(
        advapi32.ConvertSidToStringSidW,
        argtypes=(wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW,
        argtypes=(
            wintypes.LPCWSTR,
            wintypes.DWORD,
            lpvoid_pointer,
            ctypes.POINTER(wintypes.DWORD),
        ),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.GetAce,
        argtypes=(wintypes.LPVOID, wintypes.DWORD, lpvoid_pointer),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.GetAclInformation,
        argtypes=(wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.GetNamedSecurityInfoW,
        argtypes=(
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            lpvoid_pointer,
            lpvoid_pointer,
            lpvoid_pointer,
            lpvoid_pointer,
            lpvoid_pointer,
        ),
        restype=wintypes.DWORD,
    )
    _set_ctypes_signature(
        advapi32.GetSecurityDescriptorDacl,
        argtypes=(
            wintypes.LPVOID,
            ctypes.POINTER(wintypes.BOOL),
            lpvoid_pointer,
            ctypes.POINTER(wintypes.BOOL),
        ),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.GetTokenInformation,
        argtypes=(
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
        ),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.OpenProcessToken,
        argtypes=(
            wintypes.HANDLE,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.HANDLE),
        ),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        advapi32.SetNamedSecurityInfoW,
        argtypes=(
            wintypes.LPWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.LPVOID,
            wintypes.LPVOID,
            wintypes.LPVOID,
            wintypes.LPVOID,
        ),
        restype=wintypes.DWORD,
    )
    _set_ctypes_signature(
        kernel32.CloseHandle,
        argtypes=(wintypes.HANDLE,),
        restype=wintypes.BOOL,
    )
    _set_ctypes_signature(
        kernel32.GetCurrentProcess,
        argtypes=(),
        restype=wintypes.HANDLE,
    )
    _set_ctypes_signature(
        kernel32.LocalFree,
        argtypes=(wintypes.HLOCAL,),
        restype=wintypes.HLOCAL,
    )
    return advapi32, kernel32


def _apply_windows_dacl(path: Path) -> None:
    advapi32, kernel32 = _windows_security_libraries()
    current_user_sid = _current_windows_user_sid()
    sddl = f"D:P(A;;FA;;;{current_user_sid})(A;;FA;;;SY)(A;;FA;;;BA)"
    security_descriptor = wintypes.LPVOID()
    dacl = wintypes.LPVOID()
    dacl_present = wintypes.BOOL()
    dacl_defaulted = wintypes.BOOL()
    SDDL_REVISION_1 = 1
    SE_FILE_OBJECT = 1
    DACL_SECURITY_INFORMATION = 0x00000004
    PROTECTED_DACL_SECURITY_INFORMATION = 0x80000000
    if not advapi32.ConvertStringSecurityDescriptorToSecurityDescriptorW(
        sddl,
        SDDL_REVISION_1,
        ctypes.byref(security_descriptor),
        None,
    ):
        raise ProviderCredentialStoreProtectionError(
            validation_category="windows_dacl_sddl_failed",
            detail=str(ctypes.get_last_error()),
        )
    try:
        if not advapi32.GetSecurityDescriptorDacl(
            security_descriptor,
            ctypes.byref(dacl_present),
            ctypes.byref(dacl),
            ctypes.byref(dacl_defaulted),
        ):
            raise ProviderCredentialStoreProtectionError(
                validation_category="windows_dacl_extract_failed",
                detail=str(ctypes.get_last_error()),
            )
        if not dacl_present.value or not dacl.value:
            raise ProviderCredentialStoreProtectionError(
                validation_category="windows_dacl_missing_after_sddl"
            )
        security_info = DACL_SECURITY_INFORMATION | PROTECTED_DACL_SECURITY_INFORMATION
        result = advapi32.SetNamedSecurityInfoW(
            str(path),
            SE_FILE_OBJECT,
            security_info,
            None,
            None,
            dacl,
            None,
        )
        if result != 0:
            raise ProviderCredentialStoreProtectionError(
                validation_category="windows_dacl_apply_failed",
                detail=str(result),
            )
    finally:
        if security_descriptor.value:
            kernel32.LocalFree(security_descriptor)


def _sid_to_string(sid_pointer: int) -> str:
    advapi32, kernel32 = _windows_security_libraries()
    string_sid = wintypes.LPWSTR()
    if not advapi32.ConvertSidToStringSidW(
        wintypes.LPVOID(sid_pointer), ctypes.byref(string_sid)
    ):
        raise OSError(ctypes.get_last_error())
    try:
        return string_sid.value or ""
    finally:
        kernel32.LocalFree(ctypes.cast(string_sid, wintypes.HLOCAL))


def _current_windows_user_sid() -> str:
    advapi32, kernel32 = _windows_security_libraries()
    token = wintypes.HANDLE()
    TOKEN_QUERY = 0x0008
    if not advapi32.OpenProcessToken(
        kernel32.GetCurrentProcess(), TOKEN_QUERY, ctypes.byref(token)
    ):
        raise OSError(ctypes.get_last_error())
    try:
        TokenUser = 1
        needed = wintypes.DWORD(0)
        advapi32.GetTokenInformation(token, TokenUser, None, 0, ctypes.byref(needed))
        if needed.value <= 0:
            raise OSError(ctypes.get_last_error())
        buffer = ctypes.create_string_buffer(needed.value)
        if not advapi32.GetTokenInformation(
            token,
            TokenUser,
            buffer,
            needed.value,
            ctypes.byref(needed),
        ):
            raise OSError(ctypes.get_last_error())

        class SidAndAttributes(ctypes.Structure):
            _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]

        class TokenUserBuffer(ctypes.Structure):
            _fields_ = [("User", SidAndAttributes)]

        sid_pointer = ctypes.cast(
            buffer, ctypes.POINTER(TokenUserBuffer)
        ).contents.User.Sid
        if sid_pointer is None:
            raise OSError("missing token user sid")
        return _sid_to_string(sid_pointer)
    finally:
        kernel32.CloseHandle(token)


def _read_windows_allowed_dacl_sids(path: Path) -> set[str]:
    advapi32, kernel32 = _windows_security_libraries()
    SE_FILE_OBJECT = 1
    DACL_SECURITY_INFORMATION = 0x00000004
    security_descriptor = wintypes.LPVOID()
    dacl = wintypes.LPVOID()
    result = advapi32.GetNamedSecurityInfoW(
        str(path),
        SE_FILE_OBJECT,
        DACL_SECURITY_INFORMATION,
        None,
        None,
        ctypes.byref(dacl),
        None,
        ctypes.byref(security_descriptor),
    )
    if result != 0:
        raise OSError(result)
    try:
        if not dacl.value:
            raise OSError("missing dacl")

        class AclSizeInformation(ctypes.Structure):
            _fields_ = [
                ("AceCount", ctypes.c_uint32),
                ("AclBytesInUse", ctypes.c_uint32),
                ("AclBytesFree", ctypes.c_uint32),
            ]

        class AceHeader(ctypes.Structure):
            _fields_ = [
                ("AceType", ctypes.c_ubyte),
                ("AceFlags", ctypes.c_ubyte),
                ("AceSize", ctypes.c_ushort),
            ]

        info = AclSizeInformation()
        if not advapi32.GetAclInformation(
            dacl,
            ctypes.byref(info),
            ctypes.sizeof(info),
            2,
        ):
            raise OSError(ctypes.get_last_error())
        allowed_sids: set[str] = set()
        ACCESS_ALLOWED_ACE_TYPE = 0
        INHERIT_ONLY_ACE = 0x08
        for index in range(info.AceCount):
            ace = ctypes.c_void_p()
            if not advapi32.GetAce(dacl, index, ctypes.byref(ace)):
                raise OSError(ctypes.get_last_error())
            header = AceHeader.from_address(ace.value)
            if header.AceFlags & INHERIT_ONLY_ACE:
                continue
            if header.AceType != ACCESS_ALLOWED_ACE_TYPE:
                continue
            allowed_sids.add(_sid_to_string(int(ace.value) + 8))
        return allowed_sids
    finally:
        if security_descriptor.value:
            kernel32.LocalFree(security_descriptor)


def _derive_token_status(
    access_token: str,
    refresh_token: str,
    *,
    now: datetime | None = None,
) -> ProviderClientTokenStatus:
    try:
        return derive_openai_codex_client_token_status(
            access_token=SecretStr(access_token),
            refresh_token=SecretStr(refresh_token),
            now=now,
        )
    except ProviderClientTokenMetadataError as exc:
        raise InvalidProviderCredentialStoreError(
            validation_category=exc.code
        ) from None


def extract_openai_codex_oauth_credential_from_auth_store_payload(
    auth_store: dict[str, Any],
    *,
    require_governed_entry: bool = False,
    now: datetime | None = None,
) -> OpenAICodexOAuthCredential:
    """Validate one Hermes 0.19 pool entry and return its secret-bearing token pair."""

    allowed_top_level = {
        "active_provider",
        "credential_pool",
        "providers",
        "suppressed_sources",
        "updated_at",
        "version",
    }
    if require_governed_entry and set(auth_store) != allowed_top_level:
        raise InvalidProviderCredentialStoreError(
            validation_category="unexpected_top_level_keys"
        )
    if auth_store.get("version") != 1:
        raise InvalidProviderCredentialStoreError(
            validation_category="version_mismatch"
        )
    if auth_store.get("active_provider") != OPENAI_CODEX_HERMES_PROVIDER_ID:
        raise InvalidProviderCredentialStoreError(
            validation_category="active_provider_mismatch"
        )
    _parse_utc(auth_store.get("updated_at"))
    providers = _require_dict(auth_store.get("providers"), "providers_not_object")
    if providers:
        raise InvalidProviderCredentialStoreError(
            validation_category="singleton_provider_state_rejected"
        )
    suppressed_raw = auth_store.get("suppressed_sources")
    if require_governed_entry:
        suppressed = _require_dict(suppressed_raw, "suppressed_sources_not_object")
    elif suppressed_raw is None:
        suppressed = {}
    else:
        suppressed = _require_dict(suppressed_raw, "suppressed_sources_not_object")
    if require_governed_entry and suppressed.get(OPENAI_CODEX_HERMES_PROVIDER_ID) != [
        _SINGLETON_SOURCE_TO_SUPPRESS
    ]:
        raise InvalidProviderCredentialStoreError(
            validation_category="singleton_source_not_suppressed"
        )
    pool = _require_dict(auth_store.get("credential_pool"), "pool_not_object")
    if set(pool) != {OPENAI_CODEX_HERMES_PROVIDER_ID}:
        raise InvalidProviderCredentialStoreError(
            validation_category="unexpected_pool_provider"
        )
    entries = pool.get(OPENAI_CODEX_HERMES_PROVIDER_ID)
    if not isinstance(entries, list):
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_entries_not_list"
        )
    if len(entries) != 1:
        raise InvalidProviderCredentialStoreError(
            validation_category="credential_count_not_one"
        )
    entry = _require_dict(entries[0], "pool_entry_not_object")
    if require_governed_entry and set(entry) != {
        "access_token",
        "auth_type",
        "base_url",
        "id",
        "label",
        "last_error_code",
        "last_error_message",
        "last_error_reason",
        "last_error_reset_at",
        "last_refresh",
        "last_status",
        "last_status_at",
        "priority",
        "refresh_token",
        "request_count",
        "source",
    }:
        raise InvalidProviderCredentialStoreError(
            validation_category="unexpected_pool_entry_keys"
        )
    if require_governed_entry and entry.get("id") != OPENAI_CODEX_CREDENTIAL_STORE_ID:
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_store_id_mismatch"
        )
    if entry.get("auth_type") != "oauth" or entry.get("source") != _FIXED_POOL_SOURCE:
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_auth_shape_mismatch"
        )
    if entry.get("base_url") != OPENAI_CODEX_PROVIDER_ENDPOINT:
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_base_url_mismatch"
        )
    if int(entry.get("priority", -1)) != 0:
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_priority_mismatch"
        )
    if entry.get("last_status") in {"dead", "exhausted"}:
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_entry_not_usable"
        )
    if require_governed_entry and entry.get("label") != OPENAI_CODEX_INTERNAL_LABEL:
        raise InvalidProviderCredentialStoreError(
            validation_category="pool_label_mismatch"
        )
    access_token = _require_token(entry.get("access_token"), "access_token_missing")
    refresh_token = _require_token(entry.get("refresh_token"), "refresh_token_missing")
    last_refresh = _parse_utc(entry.get("last_refresh"))
    token_status = _derive_token_status(access_token, refresh_token, now=now)
    if token_status.expires_at_utc is None:
        raise InvalidProviderCredentialStoreError(
            validation_category="access_token_expiry_unknown"
        )
    return OpenAICodexOAuthCredential(
        access_token=access_token,
        refresh_token=refresh_token,
        last_refresh_utc=last_refresh,
        expires_at_utc=token_status.expires_at_utc,
    )


def validate_openai_codex_auth_store_payload(
    auth_store: dict[str, Any],
    *,
    now: datetime | None = None,
) -> OpenAICodexOAuthCredential:
    """Validate the exact dedicated Hermes 0.19 pool-only auth shape."""

    return extract_openai_codex_oauth_credential_from_auth_store_payload(
        auth_store,
        require_governed_entry=True,
        now=now,
    )


def _build_auth_store(credential: OpenAICodexOAuthCredential) -> dict[str, Any]:
    access_token = credential.access_token.get_secret_value().strip()
    refresh_token = credential.refresh_token.get_secret_value().strip()
    last_refresh = _format_utc(credential.last_refresh_utc)
    entry = {
        "access_token": access_token,
        "auth_type": "oauth",
        "base_url": OPENAI_CODEX_PROVIDER_ENDPOINT,
        "id": OPENAI_CODEX_CREDENTIAL_STORE_ID,
        "label": OPENAI_CODEX_INTERNAL_LABEL,
        "last_error_code": None,
        "last_error_message": None,
        "last_error_reason": None,
        "last_error_reset_at": None,
        "last_refresh": last_refresh,
        "last_status": None,
        "last_status_at": None,
        "priority": 0,
        "refresh_token": refresh_token,
        "request_count": 0,
        "source": _FIXED_POOL_SOURCE,
    }
    return {
        "active_provider": OPENAI_CODEX_HERMES_PROVIDER_ID,
        "credential_pool": {OPENAI_CODEX_HERMES_PROVIDER_ID: [entry]},
        "providers": {},
        "suppressed_sources": {
            OPENAI_CODEX_HERMES_PROVIDER_ID: [_SINGLETON_SOURCE_TO_SUPPRESS]
        },
        "updated_at": _format_utc(_utc_now()),
        "version": 1,
    }


def _write_exclusive_file(path: Path, payload: str) -> None:
    try:
        fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, _POSIX_FILE_MODE)
    except FileExistsError:
        raise ExistingProviderCredentialStoreError(
            validation_category="durable_store_exists"
        ) from None
    except Exception as exc:
        raise ProviderCredentialStoreWriteError(
            validation_category="create_failed",
            detail=exc.__class__.__name__,
        ) from None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    except Exception as exc:
        try:
            path.unlink()
        except OSError:
            pass
        raise ProviderCredentialStoreWriteError(
            validation_category="write_failed",
            detail=exc.__class__.__name__,
        ) from None


def _remove_staging_dir(path: Path) -> None:
    if not path.exists():
        return
    for current_root, dir_names, file_names in os.walk(
        path, topdown=False, followlinks=False
    ):
        current = Path(current_root)
        for file_name in file_names:
            try:
                (current / file_name).unlink()
            except OSError:
                pass
        for dir_name in dir_names:
            try:
                (current / dir_name).rmdir()
            except OSError:
                pass
        try:
            current.rmdir()
        except OSError:
            pass


def _status_from_valid_store(
    *,
    credential: OpenAICodexOAuthCredential | None,
    token_status: ProviderClientTokenStatus | None,
    durable_store_present: bool,
    protection_valid: bool,
) -> ProviderCredentialStatus:
    return ProviderCredentialStatus(
        configured=credential is not None,
        durable_store_present=durable_store_present,
        durable_store_valid=credential is not None,
        protection_valid=protection_valid,
        provider_state_present=False,
        pool_state_present=credential is not None,
        token_pair_present=credential is not None,
        credential_count=1 if credential is not None else 0,
        active_provider_matches=credential is not None,
        last_refresh_utc=credential.last_refresh_utc
        if credential is not None
        else None,
        expires_at_utc=credential.expires_at_utc if credential is not None else None,
        client_token_status=token_status,
    )


def read_openai_codex_credential_status(
    trusted_store_root: Path,
    *,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> ProviderCredentialStatus:
    """Read a secret-free status from one trusted dedicated store root."""

    auth_file = _auth_file_for_root(trusted_store_root)
    backend = _protection_backend(protection_backend)
    if not auth_file.exists():
        return _status_from_valid_store(
            credential=None,
            token_status=None,
            durable_store_present=False,
            protection_valid=False,
        )
    backend.validate_directory(auth_file.parent)
    backend.validate_file(auth_file)
    payload = _load_json_auth_store(auth_file)
    credential = validate_openai_codex_auth_store_payload(payload, now=now)
    token_status = _derive_token_status(
        credential.access_token.get_secret_value(),
        credential.refresh_token.get_secret_value(),
        now=now,
    )
    return _status_from_valid_store(
        credential=credential,
        token_status=token_status,
        durable_store_present=True,
        protection_valid=True,
    )


def load_openai_codex_oauth_credential(
    trusted_store_root: Path,
    *,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> OpenAICodexOAuthCredential:
    """Load exactly one governed Codex OAuth credential from a dedicated store."""

    auth_file = _auth_file_for_root(trusted_store_root)
    backend = _protection_backend(protection_backend)
    backend.validate_directory(auth_file.parent)
    backend.validate_file(auth_file)
    return validate_openai_codex_auth_store_payload(
        _load_json_auth_store(auth_file), now=now
    )


def promote_openai_codex_oauth_credential(
    trusted_store_root: Path,
    credential: OpenAICodexOAuthCredential,
    *,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> ProviderCredentialStatus:
    """Atomically create the dedicated store; never merge or overwrite."""

    auth_file = _auth_file_for_root(trusted_store_root)
    if auth_file.exists():
        raise ExistingProviderCredentialStoreError(
            validation_category="durable_store_exists"
        )
    backend = _protection_backend(protection_backend)
    backend.prepare_directory(auth_file.parent)
    payload = json.dumps(_build_auth_store(credential), indent=2, sort_keys=True) + "\n"
    staging_dir = auth_file.parent / f".agent-platform-store-stage.{uuid.uuid4().hex}"
    final_created = False
    try:
        staging_dir.mkdir(mode=_POSIX_DIRECTORY_MODE)
        backend.prepare_directory(staging_dir)
        staging_file = staging_dir / _AUTH_FILE_NAME
        _write_exclusive_file(staging_file, payload)
        backend.prepare_file(staging_file)
        validate_openai_codex_auth_store_payload(
            _load_json_auth_store(staging_file), now=now
        )
        _write_exclusive_file(auth_file, payload)
        final_created = True
        backend.prepare_file(auth_file)
        validated = validate_openai_codex_auth_store_payload(
            _load_json_auth_store(auth_file),
            now=now,
        )
        token_status = _derive_token_status(
            validated.access_token.get_secret_value(),
            validated.refresh_token.get_secret_value(),
            now=now,
        )
        return _status_from_valid_store(
            credential=validated,
            token_status=token_status,
            durable_store_present=True,
            protection_valid=True,
        )
    except Exception:
        if final_created:
            try:
                auth_file.unlink()
            except OSError:
                pass
        raise
    finally:
        _remove_staging_dir(staging_dir)


def clear_local_openai_codex_credential(
    trusted_store_root: Path,
    *,
    protection_backend: StoreProtectionBackend | None = None,
    now: datetime | None = None,
) -> ProviderCredentialLocalClearResult:
    """Delete only the local governed store; this does not revoke OAuth remotely."""

    auth_file = _auth_file_for_root(trusted_store_root)
    if not auth_file.exists():
        return ProviderCredentialLocalClearResult(local_store_present_after=False)
    backend = _protection_backend(protection_backend)
    backend.validate_directory(auth_file.parent)
    backend.validate_file(auth_file)
    validate_openai_codex_auth_store_payload(_load_json_auth_store(auth_file), now=now)
    try:
        auth_file.unlink()
    except OSError as exc:
        raise ProviderCredentialStoreWriteError(
            validation_category="clear_failed",
            detail=exc.__class__.__name__,
        ) from None
    return ProviderCredentialLocalClearResult(
        local_store_present_after=auth_file.exists()
    )


def product_python_platform() -> str:
    """Expose the host platform family for tests without leaking host paths."""

    return "windows" if sys.platform == "win32" else "posix"


__all__ = [
    "ExistingProviderCredentialStoreError",
    "InvalidProviderCredentialStoreError",
    "InvalidProviderCredentialStoreRootError",
    "MissingProviderCredentialError",
    "ProviderCredentialStoreError",
    "ProviderCredentialStoreProtectionError",
    "ProviderCredentialStoreWriteError",
    "StoreProtectionBackend",
    "StoreProtectionReport",
    "clear_local_openai_codex_credential",
    "default_openai_codex_credential_store_root",
    "extract_openai_codex_oauth_credential_from_auth_store_payload",
    "load_openai_codex_oauth_credential",
    "product_python_platform",
    "promote_openai_codex_oauth_credential",
    "read_openai_codex_credential_status",
    "validate_openai_codex_auth_store_payload",
    "validate_windows_dacl_principals",
]
