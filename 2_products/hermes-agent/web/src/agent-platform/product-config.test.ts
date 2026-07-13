import { afterEach, describe, expect, it, vi } from "vitest";

import {
  getProductFeatureState,
  loadProductConfiguration,
  parseProductConfiguration,
} from "./product-config";

function validWireConfiguration(): Record<string, unknown> {
  return {
    schema_version: 1,
    product_id: "agent-platform-hermes",
    product_display_name: "AGENT PLATFORM Hermes",
    product_version: "0.1.0-dev",
    upstream_product_name: "Hermes Agent",
    upstream_version: "0.18.2",
    upstream_commit: "9de9c25f620ff7f1ce0fd5457d596052d5159596",
    feature_flags: { "agent_platform.product_ui": "disabled" },
    extension_modules: [],
    documentation_url: null,
    support_url: null,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("product configuration", () => {
  it("normalizes the validated backend contract without independent identity defaults", () => {
    const configuration = parseProductConfiguration(validWireConfiguration());

    expect(configuration.productId).toBe("agent-platform-hermes");
    expect(configuration.productVersion).not.toBe(configuration.upstreamVersion);
    expect(configuration.extensionModules).toEqual([]);
  });

  it.each(["api_key", "token", "providers", "credential_path"])(
    "rejects unknown secret or provider field %s",
    (field) => {
      const raw = { ...validWireConfiguration(), [field]: "synthetic-value" };

      expect(() => parseProductConfiguration(raw)).toThrow();
    },
  );

  it("defaults missing features to disabled and unavailable transport to unavailable", () => {
    const configuration = parseProductConfiguration(validWireConfiguration());

    expect(getProductFeatureState(configuration, "agent_platform.future")).toBe("disabled");
    expect(getProductFeatureState(null, "agent_platform.future")).toBe("unavailable");
  });

  it("rejects credentials embedded in product URLs", () => {
    const raw = {
      ...validWireConfiguration(),
      documentation_url: "https://synthetic-user:synthetic-password@example.invalid/docs",
    };

    expect(() => parseProductConfiguration(raw)).toThrow(/must not contain credentials/);
  });

  it("consumes the protected backend endpoint through the existing API client", async () => {
    vi.stubGlobal("window", { __HERMES_SESSION_TOKEN__: "synthetic-session-token" });
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        expect(input).toBe("/api/agent-platform/product-configuration");
        expect(init?.credentials).toBe("include");
        expect(new Headers(init?.headers).get("X-Hermes-Session-Token")).toBe(
          "synthetic-session-token",
        );
        return new Response(JSON.stringify(validWireConfiguration()), {
          headers: { "Content-Type": "application/json" },
          status: 200,
        });
      },
    );
    vi.stubGlobal("fetch", fetchMock);

    const configuration = await loadProductConfiguration();

    expect(configuration?.schemaVersion).toBe(1);
    expect(fetchMock).toHaveBeenCalledOnce();
  });

  it("fails closed when the response is invalid", async () => {
    vi.stubGlobal("window", {});
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response(JSON.stringify({ schema_version: 1 }), { status: 200 })),
    );

    await expect(loadProductConfiguration()).resolves.toBeNull();
  });
});
