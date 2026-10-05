import { afterEach, describe, expect, it, vi } from "vitest";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { api, fetchJSON, setManagementProfile, getManagementProfile } from "@/lib/api";
import { ProfileContext } from "@/contexts/profile-context";
import { ProfileProvider } from "@/contexts/ProfileProvider";
import { ProfileSwitcher } from "@/components/ProfileSwitcher";
import { ProfileScopeBanner } from "@/components/ProfileScopeBanner";
import { en } from "@/i18n/en";
import { loadRuntimeOverview } from "./runtime-overview/use-runtime-overview";
import { groupShellNavigation } from "./shell/navigation";

vi.mock("@/i18n", () => ({ useI18n: () => ({ t: en }) }));
const profiles = ["", "pepper-architecture-product", "pepper-implementation-product"];

afterEach(() => {
  setManagementProfile("");
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

function transport() {
  vi.stubGlobal("window", { location: { protocol: "http:", host: "localhost" } });
  const mock = vi.fn<typeof fetch>(async () => new Response("{}", { status: 200 }));
  vi.stubGlobal("fetch", mock);
  return mock;
}

describe("C77 product/global and profile/local authority", () => {
  it.each(profiles)("keeps all product control requests global for %s", async (profile) => {
    const mock = transport();
    setManagementProfile(profile);
    for (const path of ["workflow-control", "runtime-status", "product-configuration", "approvals", "approvals/id/decision", "executions", "executions/start", "future-control"]) {
      await fetchJSON(`/api/agent-platform/${path}?profile=${profile}&board=product`);
      expect(mock.mock.lastCall?.[0]).toBe(`/api/agent-platform/${path}?board=product`);
    }
  });

  it.each(profiles.slice(1))("retains profile-local API and chat scope for %s", async (profile) => {
    const mock = transport();
    setManagementProfile(profile);
    for (const path of ["config", "model/info", "skills", "mcp", "env", "status"]) {
      await fetchJSON(`/api/${path}`);
      expect(mock.mock.lastCall?.[0]).toBe(`/api/${path}?profile=${profile}`);
    }
    await api.getSessionMessages("local-session", profile);
    expect(String(mock.mock.lastCall?.[0])).toContain(`profile=${profile}`);
    const ws = new URL(await api.buildWsUrl("/api/pty", { profile }));
    expect(ws.pathname).toBe("/api/pty");
    expect(ws.searchParams.get("profile")).toBe(profile);
  });

  it("does not infer scope from an ambiguous prefix and preserves explicit local scope", async () => {
    const mock = transport();
    setManagementProfile(profiles[1]);
    await fetchJSON("/api/configuration-unclassified");
    expect(mock.mock.lastCall?.[0]).toBe("/api/configuration-unclassified");
    await fetchJSON("/api/config?profile=explicit");
    expect(mock.mock.lastCall?.[0]).toBe("/api/config?profile=explicit");
  });

  it("profile provider failure does not participate in product overview loading", async () => {
    const mock = transport();
    setManagementProfile(profiles[1]);
    mock.mockImplementation(async (url) => {
      if (String(url).startsWith("/api/status")) throw new Error("selected chat provider unavailable");
      return new Response(JSON.stringify(String(url).endsWith("workflow-control") ? { current_ticket_id: "synthetic-current" } : { version: "test" }));
    });
    await expect(fetchJSON("/api/status")).rejects.toThrow("provider unavailable");
    await expect(loadRuntimeOverview()).resolves.toEqual({ version: "test", agent_platform_workflow_control: { current_ticket_id: "synthetic-current" } });
  });

  it.each(profiles)("renders profile semantics inside the same shell for %s", (profile) => {
    const html = renderToStaticMarkup(
      <ProfileContext.Provider value={{ profile, currentProfile: "default", profiles: ["default", ...profiles.slice(1)], setProfile: vi.fn() }}>
        <ProfileSwitcher /><ProfileScopeBanner />
      </ProfileContext.Provider>,
    );
    expect(html).toContain("Active profile");
    expect(html).not.toContain("this dashboard");
    if (!profile) expect(html).toContain("Pepper Default");
    else {
      expect(html).toContain(profile);
      expect(html).toContain("Pepper governed workflow remains product-global");
      expect(html).toContain("their own provider setup");
    }
  });

  it.each(profiles)("URL profile initializes only management state and preserves navigation for %s", (profile) => {
    const html = renderToStaticMarkup(<MemoryRouter initialEntries={[`/agent-platform/overview?profile=${profile}`]}><ProfileProvider><main>one Pepper shell</main></ProfileProvider></MemoryRouter>);
    expect(html).toBe("<main>one Pepper shell</main>");
    expect(getManagementProfile()).toBe(profile);
    const groups = groupShellNavigation(
      ["/chat", "/profiles", "/cron", "/skills", "/config"].map(path => ({ path: `${path}?profile=${profile}` })),
      ["overview", "projects", "approvals", "executions", "resources"].map(path => ({ path: `/agent-platform/${path}?profile=${profile}`, groupId: "agent-platform" as const })), {},
    );
    expect(groups.map(g => g.id)).toEqual(["control", "work", "agents", "automation", "resources", "system"]);
    expect(groups.find(g => g.id === "work")?.items).toHaveLength(3);
  });
});
