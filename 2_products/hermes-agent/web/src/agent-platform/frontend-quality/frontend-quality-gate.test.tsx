import { readFileSync } from "node:fs";
import { renderToStaticMarkup } from "react-dom/server";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

import { AGENT_PLATFORM_EXTENSIONS } from "../extensions";
import {
  parseProjectSource,
  parseProjectsSource,
  type ProjectsWorkspaceDataState,
  type ProjectsWorkspaceView,
} from "../projects-tickets/contract";
import { ProjectDetailView } from "../projects-tickets/project-detail-page";
import {
  createProjectsWorkspacePoller,
  PROJECTS_WORKSPACE_REQUEST_TIMEOUT_MS,
} from "../projects-tickets/use-projects-workspace";
import {
  createApprovalInboxPoller,
  APPROVAL_INBOX_REQUEST_TIMEOUT_MS,
} from "../approval-inbox/use-approval-inbox";
import {
  createExecutionInspectorPoller,
  EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS,
} from "../execution-inspector/use-execution-inspector";
import {
  createRuntimeOverviewPoller,
  RUNTIME_OVERVIEW_REQUEST_TIMEOUT_MS,
} from "../runtime-overview/use-runtime-overview";
import {
  FRONTEND_QUALITY_ACTIVATION,
  FRONTEND_QUALITY_DESCRIPTOR_IDS,
  FRONTEND_QUALITY_GATE_RESULT,
  FRONTEND_QUALITY_KEYBOARD_CHECKS,
  FRONTEND_QUALITY_SECURITY_CHECKS,
  FRONTEND_QUALITY_SEMANTIC_CHECKS,
  FRONTEND_QUALITY_SURFACES,
  FRONTEND_QUALITY_THEMES,
  FRONTEND_QUALITY_VIEWPORTS,
} from "./quality-matrix";
import type { FrontendQualityAllowedAction } from "./quality-contract";

afterEach(() => {
  vi.clearAllTimers();
  vi.useRealTimers();
  vi.restoreAllMocks();
});

function readyProjectState(snapshot: ProjectsWorkspaceView): ProjectsWorkspaceDataState {
  return Object.freeze({ phase: "ready", snapshot, lastSuccessAt: 1_700_000_000_000, refreshing: false });
}

function createOtherStatusProject(): ProjectsWorkspaceView {
  const project = parseProjectsSource({
    boards: [{ slug: "alpha-board", name: "Alpha Board", counts: {}, description: null }],
  })?.[0];
  expect(project).toBeTruthy();
  const detail = parseProjectSource(
    {
      columns: [
        {
          name: "source-review-needed",
          tasks: [{
            id: "t_other01",
            title: "Unknown source status ticket",
            body: "Safe bounded body",
            status: "needs-human-review",
            priority: 3,
            link_counts: { parents: 0, children: 0 },
          }],
        },
      ],
    },
    project!,
  );
  expect(detail).toBeTruthy();
  expect(detail?.tickets[0]?.visualStatus).toBe("other");
  return { kind: "project", project: detail! };
}

interface QualityPoller {
  readonly start: () => Promise<boolean>;
  readonly stop: () => void;
}

interface QualityPublishedState {
  readonly phase: string;
  readonly refreshing: boolean;
}

async function expectIgnoredCancellationToSettle(
  createPoller: (publish: (state: QualityPublishedState) => void) => QualityPoller,
  timeoutMs: number,
) {
  vi.useFakeTimers();
  const published: QualityPublishedState[] = [];
  const poller = createPoller((state) => { published.push(state); });
  const pending = poller.start();
  await vi.advanceTimersByTimeAsync(timeoutMs);
  await expect(pending).resolves.toBe(false);
  expect(published.length).toBeGreaterThan(0);
  expect(published.at(-1)).toMatchObject({ phase: "error", refreshing: false });
  poller.stop();
}

describe("P13.8 frontend quality evidence matrix", () => {
  it("aligns every quality surface route with the compiled inactive descriptor catalog", () => {
    const descriptorsById = new Map(AGENT_PLATFORM_EXTENSIONS.map((descriptor) => [descriptor.id, descriptor]));
    expect(FRONTEND_QUALITY_DESCRIPTOR_IDS).toEqual(AGENT_PLATFORM_EXTENSIONS.map((descriptor) => descriptor.id));
    expect(FRONTEND_QUALITY_ACTIVATION).toEqual({
      compiledDescriptorCount: AGENT_PLATFORM_EXTENSIONS.length,
      resolvedDescriptorCount: 0,
      runtimeRouteCount: 0,
      navigationItemCount: 0,
      productUiFeature: "disabled",
      extensionModules: [],
    });

    for (const surface of FRONTEND_QUALITY_SURFACES) {
      expect(surface.states).toContain("ready");
      expect(surface.allowedActions.length).toBeGreaterThan(0);
      expect(surface.forbiddenCapabilities).toEqual(expect.arrayContaining([
        "work-mutation",
        "approval-decision",
        "execution-control",
        "feature-toggle",
        "secret-input",
        "raw-config",
      ]));
      for (const route of surface.routes) {
        const descriptor = descriptorsById.get(route.descriptorId);
        expect(descriptor).toBeDefined();
        expect(route.path).toBe(descriptor?.route.path);
        expect(descriptor).toMatchObject({
          owner: "AGENT_PLATFORM",
          featureId: "agent_platform.product_ui",
          visibleWhenExperimental: true,
        });
        expect(route.path).toMatch(/^\/agent-platform\//);
        if (route.navigation === "top-level") expect(descriptor?.navigation).toBeDefined();
        if (route.navigation === "contextual") expect(descriptor?.navigation).toBeUndefined();
      }
    }
  });

  it("keeps the quality contract immutable and evidence-backed", () => {
    expect(Object.isFrozen(FRONTEND_QUALITY_GATE_RESULT)).toBe(true);
    expect(Object.isFrozen(FRONTEND_QUALITY_SURFACES)).toBe(true);
    for (const surface of FRONTEND_QUALITY_SURFACES) {
      expect(Object.isFrozen(surface)).toBe(true);
      expect(Object.isFrozen(surface.routes)).toBe(true);
      expect(Object.isFrozen(surface.states)).toBe(true);
      expect(Object.isFrozen(surface.allowedActions)).toBe(true);
      expect(Object.isFrozen(surface.forbiddenCapabilities)).toBe(true);
      expect(surface.evidence.length).toBeGreaterThan(0);
      expect(surface.authority).toMatch(/read-only|provisional|inactive|not |no |Validated|source-local|excluded/i);
    }
    expect(FRONTEND_QUALITY_VIEWPORTS.some((viewport) => viewport.automated)).toBe(true);
    expect(FRONTEND_QUALITY_THEMES.map((theme) => theme.id)).toEqual(["hermes-teal", "nous-blue"]);
    expect(FRONTEND_QUALITY_SEMANTIC_CHECKS.every((check) => check.evidence.length > 0)).toBe(true);
    expect(FRONTEND_QUALITY_KEYBOARD_CHECKS.flatMap((check) => check.controls)).toEqual(
      expect.arrayContaining(["refresh", "filter", "navigate", "trusted-display-write"] satisfies FrontendQualityAllowedAction[]),
    );
    expect(FRONTEND_QUALITY_SECURITY_CHECKS.flatMap((check) => check.forbiddenPatterns)).toEqual(
      expect.arrayContaining(["SECRET_", "token", "raw_yaml", "Stop execution"]),
    );
  });
});

describe("P13.8 conditional frontend fixes", () => {
  it("settles all recursive pollers when the underlying request ignores cancellation", async () => {
    await expectIgnoredCancellationToSettle(
      (publish) => createRuntimeOverviewPoller(() => new Promise<never>(() => {}), publish),
      RUNTIME_OVERVIEW_REQUEST_TIMEOUT_MS,
    );
    await expectIgnoredCancellationToSettle(
      (publish) => createProjectsWorkspacePoller(() => new Promise<never>(() => {}), publish),
      PROJECTS_WORKSPACE_REQUEST_TIMEOUT_MS,
    );
    await expectIgnoredCancellationToSettle(
      (publish) => createApprovalInboxPoller(() => new Promise<never>(() => {}), publish),
      APPROVAL_INBOX_REQUEST_TIMEOUT_MS,
    );
    await expectIgnoredCancellationToSettle(
      (publish) => createExecutionInspectorPoller(() => new Promise<never>(() => {}), publish),
      EXECUTION_INSPECTOR_REQUEST_TIMEOUT_MS,
    );
  });

  it("renders the unknown Kanban status column instead of hiding safe source tickets", () => {
    const markup = renderToStaticMarkup(
      <MemoryRouter>
        <ProjectDetailView state={readyProjectState(createOtherStatusProject())} profile="review-profile" refresh={() => {}} />
      </MemoryRouter>,
    );
    expect(markup).toContain("Hermes status: other");
    expect(markup).toContain("needs-human-review");
    expect(markup).toContain("Unrecognized Hermes source state");
    expect(markup).toContain("Source: Hermes Kanban");
  });

  it("keeps native filter selects visibly focusable through wrapper focus rings", () => {
    const sources = [
      readFileSync(new URL("../projects-tickets/projects-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../approval-inbox/approval-inbox-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../execution-inspector/execution-inspector-page.tsx", import.meta.url), "utf8"),
    ];
    for (const source of sources) {
      expect(source).toContain("focus-within:border-[var(--agent-platform-action-primary)]");
      expect(source).toContain("focus-within:ring-2");
      expect(source).toContain("focus-within:ring-[var(--agent-platform-focus-ring)]");
      expect(source).toContain("<select");
    }
  });

  it("does not add nested main landmarks inside the dashboard shell main", () => {
    const sources = [
      readFileSync(new URL("../runtime-overview/runtime-overview-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../projects-tickets/projects-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../projects-tickets/project-detail-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../projects-tickets/ticket-detail-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../approval-inbox/approval-inbox-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../approval-inbox/approval-detail-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../execution-inspector/execution-inspector-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../execution-inspector/execution-detail-page.tsx", import.meta.url), "utf8"),
      readFileSync(new URL("../safe-settings/safe-settings-page.tsx", import.meta.url), "utf8"),
    ];
    for (const source of sources) {
      expect(source).not.toContain("<main");
      expect(source).not.toContain("</main>");
    }
  });
});
