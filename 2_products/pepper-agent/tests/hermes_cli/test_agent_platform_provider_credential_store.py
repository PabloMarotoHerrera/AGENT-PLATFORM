from __future__ import annotations

import base64
import ctypes
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hermes_cli.agent_platform.provider_credentials.contracts import (
    OPENAI_CODEX_CREDENTIAL_STORE_ID,
    OPENAI_CODEX_INTERNAL_LABEL,
    OPENAI_CODEX_PROVIDER_ENDPOINT,
    OpenAICodexOAuthCredential,
)
from hermes_cli.agent_platform.provider_credentials import store
from hermes_cli.agent_platform.provider_credentials.store import (
    ExistingProviderCredentialStoreError,
    InvalidProviderCredentialStoreError,
    InvalidProviderCredentialStoreRootError,
    ProviderCredentialStoreProtectionError,
    clear_local_openai_codex_credential,
    default_openai_codex_credential_store_root,
    extract_openai_codex_oauth_credential_from_auth_store_payload,
    promote_openai_codex_oauth_credential,
    read_openai_codex_credential_status,
    validate_windows_dacl_principals,
)


NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)
SOURCE_PATH = (
    Path(__file__).resolve().parents[2]
    / "hermes_cli"
    / "agent_platform"
    / "provider_credentials"
    / "store.py"
)


class FakeProtectionBackend:
    def __init__(self, *, fail_stage_file: bool = False) -> None:
        self.fail_stage_file = fail_stage_file
        self.calls: list[tuple[str, str]] = []

    def prepare_directory(self, path: Path):
        self.calls.append(("prepare_directory", path.name))
        path.mkdir(parents=True, exist_ok=True)
        return store.StoreProtectionReport("store_directory", "test", True)

    def prepare_file(self, path: Path):
        self.calls.append(("prepare_file", path.name))
        if self.fail_stage_file and ".agent-platform-store-stage." in str(path.parent):
            raise ProviderCredentialStoreProtectionError(
                validation_category="synthetic_stage_failure"
            )
        return store.StoreProtectionReport("auth_file", "test", True)

    def validate_directory(self, path: Path):
        self.calls.append(("validate_directory", path.name))
        if not path.is_dir():
            raise ProviderCredentialStoreProtectionError(
                validation_category="missing_directory"
            )
        return store.StoreProtectionReport("store_directory", "test", True)

    def validate_file(self, path: Path):
        self.calls.append(("validate_file", path.name))
        if not path.is_file():
            raise ProviderCredentialStoreProtectionError(
                validation_category="missing_file"
            )
        return store.StoreProtectionReport("auth_file", "test", True)


def synthetic_access_token(*, exp_delta: timedelta = timedelta(hours=1)) -> str:
    payload = {
        "iat": int(NOW.timestamp()),
        "exp": int((NOW + exp_delta).timestamp()),
    }
    return ".".join((_segment({"alg": "none"}), _segment(payload), "signature"))


def _segment(payload: dict[str, object]) -> str:
    return (
        base64.urlsafe_b64encode(
            json.dumps(payload, separators=(",", ":")).encode("utf-8")
        )
        .decode("ascii")
        .rstrip("=")
    )


def synthetic_credential(
    *, expires_delta: timedelta = timedelta(hours=1)
) -> OpenAICodexOAuthCredential:
    return OpenAICodexOAuthCredential(
        access_token=synthetic_access_token(exp_delta=expires_delta),
        refresh_token="synthetic-refresh-token",
        last_refresh_utc=NOW,
        expires_at_utc=NOW + expires_delta,
    )


def test_default_durable_root_is_isolated_below_hermes_home(tmp_path: Path) -> None:
    root = default_openai_codex_credential_store_root(tmp_path / "hermes-home")
    assert root == (
        tmp_path
        / "hermes-home"
        / "agent-platform"
        / "provider-credentials"
        / "openai-codex.primary"
    )
    relative_segments = root.relative_to(tmp_path / "hermes-home").parts
    assert relative_segments == (
        "agent-platform",
        "provider-credentials",
        "openai-codex.primary",
    )
    assert relative_segments.count("agent-platform") == 1
    assert relative_segments.count("provider-credentials") == 1
    assert relative_segments.count("openai-codex.primary") == 1


def test_legacy_duplicated_root_layout_is_distinct_and_bounded(tmp_path: Path) -> None:
    hermes_home = tmp_path / "hermes-home"
    canonical = store._canonical_openai_codex_credential_store_root(hermes_home)
    legacy = store._legacy_duplicated_openai_codex_credential_store_root(hermes_home)

    assert canonical == (
        hermes_home / "agent-platform" / "provider-credentials" / "openai-codex.primary"
    )
    assert legacy == (
        hermes_home
        / "agent-platform"
        / "provider-credentials"
        / "agent-platform"
        / "provider-credentials"
        / "openai-codex.primary"
    )
    assert canonical != legacy
    assert canonical.is_relative_to(hermes_home)
    assert legacy.is_relative_to(hermes_home)


def test_default_root_resolution_prefers_canonical_for_new_or_canonical_store(
    tmp_path: Path,
) -> None:
    hermes_home = tmp_path / "hermes-home"
    canonical = store._canonical_openai_codex_credential_store_root(hermes_home)

    assert default_openai_codex_credential_store_root(hermes_home) == canonical
    assert not hermes_home.exists()

    canonical.mkdir(parents=True)
    assert default_openai_codex_credential_store_root(hermes_home) == canonical


def test_default_root_resolution_keeps_legacy_only_store_discoverable(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    hermes_home = tmp_path / "hermes-home"
    legacy = store._legacy_duplicated_openai_codex_credential_store_root(hermes_home)
    legacy.mkdir(parents=True)
    (legacy / "auth.json").write_text("not-json-but-not-read\n", encoding="utf-8")
    monkeypatch.setattr(
        store,
        "_load_json_auth_store",
        lambda _path: pytest.fail("resolver must not read auth.json"),
    )

    assert default_openai_codex_credential_store_root(hermes_home) == legacy
    assert not store._canonical_openai_codex_credential_store_root(hermes_home).exists()


def test_default_root_resolution_fails_closed_when_both_layouts_exist(
    tmp_path: Path,
) -> None:
    hermes_home = tmp_path / "hermes-home"
    canonical = store._canonical_openai_codex_credential_store_root(hermes_home)
    legacy = store._legacy_duplicated_openai_codex_credential_store_root(hermes_home)
    canonical.mkdir(parents=True)
    legacy.mkdir(parents=True)

    with pytest.raises(InvalidProviderCredentialStoreRootError) as exc_info:
        default_openai_codex_credential_store_root(hermes_home)
    assert (
        exc_info.value.validation_category
        == "ambiguous_canonical_and_legacy_credential_store_roots"
    )


def test_root_resolver_creates_no_layout_and_malformed_root_validates_later(
    tmp_path: Path,
) -> None:
    hermes_home = tmp_path / "hermes-home"
    canonical = store._canonical_openai_codex_credential_store_root(hermes_home)

    selected = default_openai_codex_credential_store_root(hermes_home)

    assert selected == canonical
    assert not canonical.exists()
    assert not hermes_home.exists()

    canonical.parent.mkdir(parents=True)
    canonical.write_text("synthetic malformed root\n", encoding="utf-8")
    assert store._store_root_layout_present(canonical) is True
    assert default_openai_codex_credential_store_root(hermes_home) == canonical
    with pytest.raises(InvalidProviderCredentialStoreRootError) as exc_info:
        read_openai_codex_credential_status(
            canonical,
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )
    assert exc_info.value.validation_category == "not_directory"


def test_p15c1_windows_protection_helpers_remain_present() -> None:
    for helper_name in (
        "_windows_security_libraries",
        "_apply_windows_dacl",
        "_sid_to_string",
        "_current_windows_user_sid",
        "_read_windows_allowed_dacl_sids",
        "_validate_windows_dacl",
        "validate_windows_dacl_principals",
    ):
        assert hasattr(store, helper_name)


def test_status_for_missing_store_is_secret_free_and_read_only(tmp_path: Path) -> None:
    trusted_root = tmp_path / "dedicated-store"
    status = read_openai_codex_credential_status(
        trusted_root,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert status.configured is False
    assert status.durable_store_present is False
    assert status.credential_count == 0
    assert status.client_token_status is None
    assert not (trusted_root / "auth.json").exists()


def test_promote_creates_exact_single_pool_only_store_and_clear_is_local_only(
    tmp_path: Path,
) -> None:
    trusted_root = tmp_path / "dedicated-store"
    fake = FakeProtectionBackend()
    status = promote_openai_codex_oauth_credential(
        trusted_root,
        synthetic_credential(),
        protection_backend=fake,
        now=NOW,
    )
    payload = json.loads((trusted_root / "auth.json").read_text(encoding="utf-8"))

    assert status.configured is True
    assert status.credential_count == 1
    assert status.provider_state_present is False
    assert status.pool_state_present is True
    assert status.client_token_status is not None
    assert status.client_token_status.usable_for_bounded_lease is True
    assert payload["providers"] == {}
    assert payload["suppressed_sources"] == {"openai-codex": ["device_code"]}
    assert set(payload["credential_pool"]) == {"openai-codex"}
    assert payload["active_provider"] == "openai-codex"
    pool_entries = payload["credential_pool"]["openai-codex"]
    assert len(pool_entries) == 1
    assert pool_entries[0]["id"] == OPENAI_CODEX_CREDENTIAL_STORE_ID
    assert pool_entries[0]["label"] == OPENAI_CODEX_INTERNAL_LABEL
    assert pool_entries[0]["source"] == "manual:device_code"
    assert pool_entries[0]["auth_type"] == "oauth"
    assert pool_entries[0]["base_url"] == OPENAI_CODEX_PROVIDER_ENDPOINT
    assert pool_entries[0]["priority"] == 0
    assert any(call[0] == "prepare_file" for call in fake.calls)

    clear_result = clear_local_openai_codex_credential(
        trusted_root,
        protection_backend=fake,
        now=NOW,
    )
    assert clear_result.local_store_present_after is False
    assert clear_result.remote_revocation == "not_supported_or_unverified"
    assert not (trusted_root / "auth.json").exists()


def test_acquisition_pool_shape_can_be_extracted_then_promoted(tmp_path: Path) -> None:
    payload = {
        "version": 1,
        "updated_at": NOW.isoformat().replace("+00:00", "Z"),
        "active_provider": "openai-codex",
        "providers": {},
        "credential_pool": {
            "openai-codex": [
                {
                    "id": "abc123",
                    "label": "source-derived",
                    "auth_type": "oauth",
                    "priority": 0,
                    "source": "manual:device_code",
                    "access_token": synthetic_access_token(),
                    "refresh_token": "synthetic-refresh-token",
                    "base_url": "https://chatgpt.com/backend-api/codex",
                    "last_refresh": NOW.isoformat().replace("+00:00", "Z"),
                }
            ],
        },
    }
    credential = extract_openai_codex_oauth_credential_from_auth_store_payload(
        payload,
        now=NOW,
    )
    status = promote_openai_codex_oauth_credential(
        tmp_path / "durable",
        credential,
        protection_backend=FakeProtectionBackend(),
        now=NOW,
    )

    assert status.configured is True
    assert status.client_token_status is not None
    assert status.client_token_status.remote_validity == "unverified"


def test_existing_durable_store_is_rejected_without_overwrite(tmp_path: Path) -> None:
    trusted_root = tmp_path / "dedicated-store"
    trusted_root.mkdir()
    auth_file = trusted_root / "auth.json"
    original = '{"preexisting": true}\n'
    auth_file.write_text(original, encoding="utf-8")

    with pytest.raises(ExistingProviderCredentialStoreError):
        promote_openai_codex_oauth_credential(
            trusted_root,
            synthetic_credential(),
            protection_backend=FakeProtectionBackend(),
            now=NOW,
        )

    assert auth_file.read_text(encoding="utf-8") == original


def test_unrelated_singleton_and_multiple_codex_credentials_are_rejected(
    tmp_path: Path,
) -> None:
    fake = FakeProtectionBackend()
    root = tmp_path / "bad-store"
    promote_openai_codex_oauth_credential(
        root,
        synthetic_credential(),
        protection_backend=fake,
        now=NOW,
    )
    payload = json.loads((root / "auth.json").read_text(encoding="utf-8"))
    payload["providers"]["openai-codex"] = {"tokens": {"access_token": "bad"}}
    (root / "auth.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidProviderCredentialStoreError):
        read_openai_codex_credential_status(root, protection_backend=fake, now=NOW)

    root2 = tmp_path / "multiple-store"
    promote_openai_codex_oauth_credential(
        root2,
        synthetic_credential(),
        protection_backend=fake,
        now=NOW,
    )
    payload = json.loads((root2 / "auth.json").read_text(encoding="utf-8"))
    payload["credential_pool"]["openai-codex"].append({
        **payload["credential_pool"]["openai-codex"][0],
        "id": "second",
    })
    (root2 / "auth.json").write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(InvalidProviderCredentialStoreError):
        read_openai_codex_credential_status(root2, protection_backend=fake, now=NOW)


def test_failed_staging_validation_leaves_no_store_or_stage_residue(
    tmp_path: Path,
) -> None:
    trusted_root = tmp_path / "dedicated-store"

    with pytest.raises(ProviderCredentialStoreProtectionError):
        promote_openai_codex_oauth_credential(
            trusted_root,
            synthetic_credential(),
            protection_backend=FakeProtectionBackend(fail_stage_file=True),
            now=NOW,
        )

    assert not (trusted_root / "auth.json").exists()
    assert not list(trusted_root.glob(".agent-platform-store-stage.*"))


def test_windows_dacl_policy_rejects_broad_or_unknown_principals() -> None:
    current = "S-1-5-21-1000"
    report = validate_windows_dacl_principals(
        {current, "S-1-5-18"}, current_user_sid=current
    )
    assert report.protected is True
    for forbidden in ("S-1-1-0", "S-1-5-11", "S-1-5-32-545"):
        with pytest.raises(ProviderCredentialStoreProtectionError):
            validate_windows_dacl_principals(
                {current, forbidden}, current_user_sid=current
            )
    with pytest.raises(ProviderCredentialStoreProtectionError):
        validate_windows_dacl_principals(
            {current, "S-1-5-21-unknown"}, current_user_sid=current
        )
    with pytest.raises(ProviderCredentialStoreProtectionError):
        validate_windows_dacl_principals({"S-1-5-18"}, current_user_sid=current)


def test_windows_dacl_backend_uses_typed_native_handles(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    current_sid = "S-1-5-21-1000"
    system_sid = "S-1-5-18"
    admin_sid = "S-1-5-32-544"
    process_handle = 0x1234567887654321
    token_handle = 0x2234567898765432
    dacl_handle = 0x3334567898765432
    security_descriptor = 0x4434567898765432
    token_sid_pointer = 0x5534567898765432
    sid_by_pointer = {token_sid_pointer: current_sid}
    closed_handles: list[int] = []
    freed_handles: list[int] = []
    applied_sddl: list[str] = []
    set_named_security_info_calls: list[tuple[str, int, int]] = []

    class FakeFunction:
        def __init__(self, implementation):
            self.implementation = implementation
            self.argtypes = None
            self.restype = None

        def __call__(self, *args):
            return self.implementation(self, *args)

    class FakeAccessAllowedAce(ctypes.Structure):
        _fields_ = [
            ("AceType", ctypes.c_ubyte),
            ("AceFlags", ctypes.c_ubyte),
            ("AceSize", ctypes.c_ushort),
            ("Mask", ctypes.c_uint32),
            ("SidStart", ctypes.c_uint32),
        ]

    ace_buffers = [
        FakeAccessAllowedAce(0, 0, ctypes.sizeof(FakeAccessAllowedAce), 0, 0),
        FakeAccessAllowedAce(0, 0, ctypes.sizeof(FakeAccessAllowedAce), 0, 0),
        FakeAccessAllowedAce(0, 0, ctypes.sizeof(FakeAccessAllowedAce), 0, 0),
    ]
    sid_by_pointer[ctypes.addressof(ace_buffers[0]) + 8] = current_sid
    sid_by_pointer[ctypes.addressof(ace_buffers[1]) + 8] = system_sid
    sid_by_pointer[ctypes.addressof(ace_buffers[2]) + 8] = admin_sid

    def handle_value(value):
        if hasattr(value, "value"):
            return value.value
        return value

    def convert_sid_to_string(fn, sid_pointer, string_sid_out):
        assert fn.restype is store.wintypes.BOOL
        string_sid_out._obj.value = sid_by_pointer[handle_value(sid_pointer)]
        return 1

    def convert_sddl_to_security_descriptor(
        fn,
        sddl,
        revision,
        security_descriptor_out,
        descriptor_size_out,
    ):
        assert fn.restype is store.wintypes.BOOL
        assert revision == 1
        assert descriptor_size_out is None
        assert sddl == f"D:P(A;;FA;;;{current_sid})(A;;FA;;;SY)(A;;FA;;;BA)"
        applied_sddl.append(sddl)
        security_descriptor_out._obj.value = security_descriptor
        return 1

    def get_named_security_info(fn, path, object_type, security_info, *outputs):
        assert fn.restype is store.wintypes.DWORD
        assert path.endswith("auth.json")
        assert object_type == 1
        assert security_info == 0x00000004
        outputs[2]._obj.value = dacl_handle
        outputs[4]._obj.value = security_descriptor
        return 0

    def get_acl_information(fn, dacl, info_out, _info_size, info_class):
        assert fn.restype is store.wintypes.BOOL
        assert handle_value(dacl) == dacl_handle
        assert info_class == 2
        info_out._obj.AceCount = len(ace_buffers)
        return 1

    def get_security_descriptor_dacl(
        fn,
        descriptor,
        dacl_present_out,
        dacl_out,
        dacl_defaulted_out,
    ):
        assert fn.restype is store.wintypes.BOOL
        assert handle_value(descriptor) == security_descriptor
        dacl_present_out._obj.value = True
        dacl_out._obj.value = dacl_handle
        dacl_defaulted_out._obj.value = False
        return 1

    def get_ace(fn, dacl, index, ace_out):
        assert fn.restype is store.wintypes.BOOL
        assert handle_value(dacl) == dacl_handle
        ace_out._obj.value = ctypes.addressof(ace_buffers[index])
        return 1

    def get_current_process(fn):
        assert fn.restype is store.wintypes.HANDLE
        return process_handle

    def open_process_token(fn, process, access, token_out):
        assert fn.restype is store.wintypes.BOOL
        assert handle_value(process) == process_handle
        assert access == 0x0008
        token_out._obj.value = token_handle
        return 1

    def get_token_information(fn, token, token_class, buffer, buffer_size, needed_out):
        assert fn.restype is store.wintypes.BOOL
        assert handle_value(token) == token_handle
        assert token_class == 1
        if buffer is None:
            needed_out._obj.value = 32
            return 0
        assert buffer_size == 32
        ctypes.c_void_p.from_buffer(buffer).value = token_sid_pointer
        needed_out._obj.value = 32
        return 1

    def close_handle(fn, handle):
        assert fn.restype is store.wintypes.BOOL
        closed_handles.append(handle_value(handle))
        return 1

    def local_free(fn, handle):
        assert fn.restype is store.wintypes.HLOCAL
        freed_handles.append(handle_value(handle))
        return 0

    def set_named_security_info(fn, path, object_type, security_info, *args):
        assert fn.restype is store.wintypes.DWORD
        assert path.endswith("auth.json")
        assert object_type == 1
        assert security_info == 0x80000004
        owner, group, dacl, sacl = args
        assert owner is None
        assert group is None
        assert handle_value(dacl) == dacl_handle
        assert sacl is None
        set_named_security_info_calls.append((path, security_info, dacl_handle))
        return 0

    class FakeAdvapi32:
        def __init__(self) -> None:
            self.ConvertSidToStringSidW = FakeFunction(convert_sid_to_string)
            self.ConvertStringSecurityDescriptorToSecurityDescriptorW = FakeFunction(
                convert_sddl_to_security_descriptor
            )
            self.GetAce = FakeFunction(get_ace)
            self.GetAclInformation = FakeFunction(get_acl_information)
            self.GetNamedSecurityInfoW = FakeFunction(get_named_security_info)
            self.GetSecurityDescriptorDacl = FakeFunction(get_security_descriptor_dacl)
            self.GetTokenInformation = FakeFunction(get_token_information)
            self.OpenProcessToken = FakeFunction(open_process_token)
            self.SetNamedSecurityInfoW = FakeFunction(set_named_security_info)

    class FakeKernel32:
        def __init__(self) -> None:
            self.CloseHandle = FakeFunction(close_handle)
            self.GetCurrentProcess = FakeFunction(get_current_process)
            self.LocalFree = FakeFunction(local_free)

    fake_dlls = {"advapi32": FakeAdvapi32(), "kernel32": FakeKernel32()}

    def fake_windll(name: str, *, use_last_error: bool):
        assert use_last_error is True
        return fake_dlls[name]

    synthetic_path = tmp_path / "auth.json"
    synthetic_path.write_text('{"synthetic": true}\n', encoding="utf-8")
    monkeypatch.setattr(store.ctypes, "WinDLL", fake_windll, raising=False)
    monkeypatch.setattr(store.os, "name", "nt")

    report = store.StoreProtectionBackend().prepare_file(synthetic_path)

    assert report.protected is True
    assert report.dacl_inspected is True
    assert report.allowed_principal_count == 3
    assert len(set_named_security_info_calls) == 1
    assert applied_sddl == [f"D:P(A;;FA;;;{current_sid})(A;;FA;;;SY)(A;;FA;;;BA)"]
    assert closed_handles == [token_handle, token_handle]
    assert freed_handles.count(security_descriptor) == 2


def test_store_source_has_no_user_store_merge_or_provider_call_authority() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    forbidden_fragments = (
        "Path.home",
        "os.getenv",
        ".codex",
        "webbrowser",
        "subprocess",
        "_codex_device_code_login",
        "resolve_codex_runtime_credentials",
        "read_credential_pool",
        "write_credential_pool",
    )
    for fragment in forbidden_fragments:
        assert fragment not in source
    assert "credential_count_not_one" in source
    assert "singleton_provider_state_rejected" in source
    assert "windows_forbidden_principal" in source
