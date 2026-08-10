import { fetchJSON } from "@/lib/api";

import {
  validateBoardSlug,
  validateProfileName,
  validateTaskId,
} from "../projects-tickets/contract";
import {
  parseExecutionCollectionSource,
  parseExecutionDetailSource,
  validateExecutionId,
  type ExecutionInspectorRequest,
  type ExecutionInspectorView,
} from "./contract";

const EXECUTION_API_ROOT = "/api/agent-platform/executions";

export const EXECUTION_LIVE_SOURCE_CLASSIFICATION = Object.freeze({
  classification: "safe_controlled_product_source" as const,
  productionAvailability: "available" as const,
  source: "pepper-controlled-execution" as const,
  reason: "Pepper exposes authenticated universal execution collection plus exact board/task/run detail.",
  storageBehavior: "GET reads may initialize or migrate the source Kanban database" as const,
  profileBehavior: "selected profile is request context while run.profile remains a source fact" as const,
  rawTransportExposure: "authenticated product response projected immediately through an allowlist" as const,
});

function safeProfile(profile: string): string | null {
  return profile === "" ? "" : validateProfileName(profile);
}

function qualifiers(boardSlug: string, taskId: string, profile: string): URLSearchParams | null {
  const board = validateBoardSlug(boardSlug);
  const task = validateTaskId(taskId);
  const selectedProfile = safeProfile(profile);
  if (!board || !task || selectedProfile === null) return null;
  const params = new URLSearchParams({ board, task });
  if (selectedProfile) params.set("profile", selectedProfile);
  return params;
}

export function buildExecutionsPath(profile: string, boardSlug = "", taskId = ""): string | null {
  const selectedProfile = safeProfile(profile);
  if (selectedProfile === null) return null;
  if (!boardSlug && !taskId) {
    return selectedProfile
      ? `/agent-platform/executions?${new URLSearchParams({ profile: selectedProfile })}`
      : "/agent-platform/executions";
  }
  const params = qualifiers(boardSlug, taskId, profile);
  return params ? `/agent-platform/executions?${params}` : null;
}

export function buildExecutionDetailPath(
  executionId: string | number,
  boardSlug: string,
  taskId: string,
  profile: string,
): string | null {
  const id = validateExecutionId(String(executionId));
  const params = qualifiers(boardSlug, taskId, profile);
  return id && params ? `/agent-platform/executions/${encodeURIComponent(id)}?${params}` : null;
}

function isNotFound(error: unknown): boolean {
  return error instanceof Error && error.message.startsWith("404:");
}

/** Load one exact board/task source context; never fall back to the process-current board. */
export async function getQualifiedExecutionSource(
  boardSlug: string,
  taskId: string,
  profile: string,
  signal?: AbortSignal,
): Promise<unknown> {
  const board = validateBoardSlug(boardSlug);
  const task = validateTaskId(taskId);
  const selectedProfile = safeProfile(profile);
  if (!board || !task || selectedProfile === null) return null;
  try {
    const taskParams = new URLSearchParams({ board, task });
    if (selectedProfile) taskParams.set("profile", selectedProfile);
    return await fetchJSON<unknown>(
      `${EXECUTION_API_ROOT}?${taskParams}`,
      { signal },
    );
  } catch (error) {
    if (isNotFound(error)) return null;
    throw error;
  }
}

export async function getExecutionSource(
  executionId: string,
  boardSlug: string,
  taskId: string,
  profile: string,
  signal?: AbortSignal,
): Promise<unknown> {
  const id = validateExecutionId(executionId);
  const params = qualifiers(boardSlug, taskId, profile);
  if (!id || !params) return null;
  try {
    return await fetchJSON<unknown>(
      `${EXECUTION_API_ROOT}/${encodeURIComponent(id)}?${params}`,
      { signal },
    );
  } catch (error) {
    if (isNotFound(error)) return null;
    throw error;
  }
}

export async function prepareControlledExecution(
  boardSlug: string,
  taskId: string,
  profile: string,
): Promise<unknown> {
  const board = validateBoardSlug(boardSlug);
  const task = validateTaskId(taskId);
  const selectedProfile = safeProfile(profile);
  if (!board || !task || selectedProfile === null) return null;
  const params = selectedProfile ? `?${new URLSearchParams({ profile: selectedProfile })}` : "";
  return fetchJSON<unknown>(
    `${EXECUTION_API_ROOT}/start${params}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ board_slug: board, task_id: task, profile: selectedProfile || null }),
    },
  );
}

export type ExecutionInspectorLoader = (
  request: ExecutionInspectorRequest,
  profile: string,
  signal?: AbortSignal,
) => Promise<ExecutionInspectorView | null>;

export const loadExecutionInspectorRequest: ExecutionInspectorLoader = async (request, profile, signal) => {
  if (request.kind === "detail" && !validateExecutionId(request.executionId)) return null;
  const observedAt = Date.now();
  const selectedProfile = safeProfile(profile);
  if (selectedProfile === null) return null;
  if (request.kind === "executions" && !request.boardSlug && !request.taskId) {
    const params = new URLSearchParams();
    if (selectedProfile) params.set("profile", selectedProfile);
    const raw = await fetchJSON<unknown>(
      `${EXECUTION_API_ROOT}${params.toString() ? `?${params}` : ""}`,
      { signal },
    );
    const collection = parseExecutionCollectionSource(raw, "all", "all", observedAt);
    return collection ? Object.freeze({ kind: "executions", collection }) : null;
  }
  if (request.kind === "executions") {
    const raw = await getQualifiedExecutionSource(request.boardSlug, request.taskId, profile, signal);
    const collection = parseExecutionCollectionSource(
      raw,
      request.boardSlug,
      request.taskId,
      observedAt,
    );
    return collection ? Object.freeze({ kind: "executions", collection }) : null;
  }
  const raw = await getExecutionSource(request.executionId, request.boardSlug, request.taskId, profile, signal);
  const execution = parseExecutionDetailSource(
    raw,
    request.boardSlug,
    request.taskId,
    request.executionId,
    observedAt,
  );
  return execution ? Object.freeze({ kind: "detail", execution }) : null;
};
