import { afterEach, describe, expect, it, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { NewChatProfile } from "@/components/NewChatProfile";
import { ProfileProvider } from "@/contexts/ProfileProvider";
import { getManagementProfile, setManagementProfile, api, fetchJSON } from "@/lib/api";
import { chatBindingFromUrl, chatBindingParams, chatSessionPath, newChatBinding, resolveChatBinding, consumeChatLocation, managementProfileForRoute, profileDisplayName } from "@/lib/profile-context";
import { en } from "@/i18n/en";
import App from "@/App";
import { ProductConfigurationContext } from "./product-config-context";
import { parseProductConfiguration } from "./product-config";

vi.mock("@/i18n", async importOriginal => ({ ...await importOriginal<typeof import("@/i18n")>(), useI18n: () => ({ t: en, locale: "en", setLocale: vi.fn() }) }));
vi.mock("@/pages/ChatPage", () => ({ default: () => <div>Persistent PTY host</div> }));
vi.mock("@/themes", () => ({ useTheme: () => ({ theme: {}, availableThemes: [], themeName: "default", setTheme: vi.fn() }) }));
vi.mock("@/plugins", () => ({ usePlugins: () => ({ manifests: [], loading: false }), PluginSlot: () => null, PluginPage: () => null }));
vi.mock("@/contexts/useSystemActions", () => ({ useSystemActions: () => ({ pendingAction: null, runningAction: null, requestAction: vi.fn() }) }));

const architecture = "pepper-architecture-product";
const implementation = "pepper-implementation-product";
const names = ["default", architecture, implementation];
const profiles = ["", architecture, implementation];

afterEach(() => { setManagementProfile(""); vi.unstubAllGlobals(); vi.restoreAllMocks(); });

describe("C78 single shell and route-local management", () => {
  it.each(profiles)("canonical shell has no global profile selector for %s", (profile) => {
    const config = parseProductConfiguration({
      schema_version: 1, product_id: "pepper", product_display_name: "Pepper", product_version: "test",
      upstream_product_name: "Hermes Agent", upstream_version: "0.19.0", upstream_commit: "3ef6bbd201263d354fd83ec55b3c306ded2eb72a",
      feature_flags: { "agent_platform.product_ui": "enabled" },
      extension_modules: ["agent_platform.ui.overview", "agent_platform.ui.projects", "agent_platform.ui.approvals", "agent_platform.ui.executions"],
      documentation_url: null, support_url: null,
    });
    const html = renderToStaticMarkup(<MemoryRouter initialEntries={[`/agent-platform/overview?profile=${profile}`]}><ProductConfigurationContext.Provider value={config}><App /></ProductConfigurationContext.Provider></MemoryRouter>);
    expect(html).not.toContain("hermes-profile-switcher");
    expect(html).not.toContain("Active profile");
    expect(html).not.toContain("this dashboard");
    expect(html).not.toContain("Managing profile");
    for (const target of ["/profiles", "/chat", "/agent-platform/projects", "/agent-platform/approvals", "/agent-platform/executions"]) expect(html).toContain(`href="${target}"`);
    expect(getManagementProfile()).toBe("");
  });

  it.each(["/agent-platform/overview", "/chat", "/", "/cron"])("does not inherit profile on %s", (path) => {
    expect(managementProfileForRoute(path, new URLSearchParams({ profile: architecture }))).toBe("");
    renderToStaticMarkup(<MemoryRouter initialEntries={[`${path}?profile=${architecture}`]}><ProfileProvider><main>one shell</main></ProfileProvider></MemoryRouter>);
    expect(getManagementProfile()).toBe("");
  });

  it("management scope is explicit per route; bare navigation resets to process default", () => {
    expect(managementProfileForRoute("/skills", new URLSearchParams({ profile: architecture }))).toBe(architecture);
    expect(managementProfileForRoute("/config", new URLSearchParams())).toBe("");
    expect(managementProfileForRoute("/profiles", new URLSearchParams())).toBe("");
  });
});

describe("C78 chat creation and immutable binding", () => {
  it.each(profiles)("renders local new-chat choice and session identity for %s", (profile) => {
    const html = renderToStaticMarkup(<NewChatProfile profiles={names} currentProfile="default" draft={profile} boundProfile={architecture} onChange={vi.fn()} onStart={vi.fn()} />);
    expect(html).toContain("New chat profile");
    expect(html).toContain("Pepper Default");
    expect(html).toContain(`value="${architecture}"`);
    expect(html).toContain(`value="${implementation}"`);
    expect(html).toContain("Session profile: Architecture");
    expect(html).toContain("product-global");
  });

  it.each(profiles)("binds new PTY and profile-local history to %s", async profile => {
    vi.stubGlobal("window", { location: { protocol: "http:", host: "localhost" } });
    const fetchMock = vi.fn(async () => new Response("{}")); vi.stubGlobal("fetch", fetchMock);
    const bound = newChatBinding(profile);
    const ws = new URL(await api.buildWsUrl("/api/pty", Object.fromEntries(chatBindingParams(bound))));
    expect(ws.searchParams.get("profile") ?? "").toBe(profile);
    expect(ws.searchParams.has("resume")).toBe(false);
    await api.getSessionMessages("session-1", bound.profile);
    expect(new URL(String(fetchMock.mock.lastCall?.[0]), "http://localhost").searchParams.get("profile") ?? "").toBe(profile);
    await fetchJSON(`/api/agent-platform/workflow-control?profile=${profile}`);
    expect(fetchMock.mock.lastCall?.[0]).toBe("/api/agent-platform/workflow-control");
  });

  it("draft choice changes only the next chat, and inactive page/query changes cannot reassign the existing chat", () => {
    const original = chatBindingFromUrl(new URLSearchParams({ profile: architecture, resume: "original-session" }));
    let draft = "";
    let bound = original;
    const props = { profiles: names, currentProfile: "default", draft, boundProfile: bound.profile,
      onChange: (value: string) => { draft = value; }, onStart: () => { bound = newChatBinding(draft); } };
    // These are the control's actual handlers; selecting does not invoke start.
    props.onChange(implementation);
    expect(bound).toBe(original);
    expect(resolveChatBinding(bound, new URLSearchParams({ profile: implementation }), false)).toBe(original);
    expect(resolveChatBinding(bound, new URLSearchParams(), true)).toBe(original);
    props.onStart();
    expect(bound).toEqual({ profile: implementation, resume: null });
    expect(original).toEqual({ profile: architecture, resume: "original-session" });
  });

  it("resume links carry their own profile, including default and unknown profiles without fallback", () => {
    const original = newChatBinding(architecture);
    const resumed = resolveChatBinding(original, new URLSearchParams({ resume: "default-session", profile: "" }), true);
    expect(resumed).toEqual({ profile: "", resume: "default-session" });
    const unknown = chatBindingFromUrl(new URLSearchParams({ resume: "id", profile: "../../unknown" }));
    expect(unknown.profile).toBe("../../unknown");
    expect(managementProfileForRoute("/agent-platform/projects", chatBindingParams(unknown))).toBe("");
  });

  it("display names preserve canonical identities", () => {
    expect(profiles.map(profileDisplayName)).toEqual(["Pepper Default", "Architecture", "Implementation"]);
    expect(profileDisplayName("custom-profile")).toBe("custom-profile");
  });

  it("a new-chat binding wins while navigation still exposes the previous session URL", () => {
    const oldUrl = new URLSearchParams({ profile: architecture, resume: "old-session" });
    const created = { binding: newChatBinding(implementation), locationKey: "old-location" };
    expect(consumeChatLocation(created, oldUrl, true, "old-location")).toBe(created);
    const navigated = consumeChatLocation(created, chatBindingParams(created.binding), true, "new-location");
    expect(navigated.binding).toBe(created.binding);
    expect(consumeChatLocation(navigated, oldUrl, false, "management-page")).toBe(navigated);
    const returned = consumeChatLocation(navigated, new URLSearchParams(), true, "back-to-chat");
    expect(returned.binding).toBe(created.binding);
  });

  it.each(profiles)("session and skill links explicitly transport their local profile %s", profile => {
    const resume = new URL(chatSessionPath(profile, "session-id"), "http://localhost");
    expect(chatBindingFromUrl(resume.searchParams)).toEqual({ profile, resume: "session-id" });
    const learn = new URL(chatSessionPath(profile, null, "a skill & more"), "http://localhost");
    expect(learn.searchParams.has("profile")).toBe(true);
    expect(learn.searchParams.get("profile")).toBe(profile);
    expect(learn.searchParams.get("learn")).toBe("a skill & more");
  });
});
