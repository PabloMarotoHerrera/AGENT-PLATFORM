import { fetchJSON } from "@/lib/api";

import {
  parseProjectsSource,
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

const KANBAN_API_ROOT = "/api/plugins/kanban";

export const EXECUTION_LIVE_SOURCE_CLASSIFICATION = Object.freeze({
  classification: "safe_nested_partial_source" as const,
  productionAvailability: "qualified-only" as const,
  source: "hermes-kanban-task-run" as const,
  reason: "Hermes exposes task-nested Kanban runs and linked events, but no safe universal execution collection.",
  storageBehavior: "GET reads may initialize or migrate the source database" as const,
  profileBehavior: "Kanban storage is shared; selected profile is request context while run.profile is the source fact" as const,
  rawTransportExposure: "authenticated broad task response projected immediately through an allowlist" as const,
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
    const boardParams = new URLSearchParams({ include_archived: "false" });
    const taskParams = new URLSearchParams({ board });
    if (selectedProfile) {
      boardParams.set("profile", selectedProfile);
      taskParams.set("profile", selectedProfile);
    }
    const projects = parseProjectsSource(await fetchJSON<unknown>(
      `${KANBAN_API_ROOT}/boards?${boardParams}`,
      { signal },
    ));
    if (!projects?.some((project) => project.boardSlug === board)) return null;
    return await fetchJSON<unknown>(
      `${KANBAN_API_ROOT}/tasks/${encodeURIComponent(task)}?${taskParams}`,
      { signal },
    );
  } catch (error) {
    if (isNotFound(error)) return null;
    throw error;
  }
}

export type ExecutionInspectorLoader = (
  request: ExecutionInspectorRequest,
  profile: string,
  signal?: AbortSignal,
) => Promise<ExecutionInspectorView | null>;

export const loadExecutionInspectorRequest: ExecutionInspectorLoader = async (request, profile, signal) => {
  if (request.kind === "detail" && !validateExecutionId(request.executionId)) return null;
  const observedAt = Date.now();
  const raw = await getQualifiedExecutionSource(request.boardSlug, request.taskId, profile, signal);
  if (request.kind === "executions") {
    const collection = parseExecutionCollectionSource(
      raw,
      request.boardSlug,
      request.taskId,
      observedAt,
    );
    return collection ? Object.freeze({ kind: "executions", collection }) : null;
  }
  const execution = parseExecutionDetailSource(
    raw,
    request.boardSlug,
    request.taskId,
    request.executionId,
    observedAt,
  );
  return execution ? Object.freeze({ kind: "detail", execution }) : null;
};
