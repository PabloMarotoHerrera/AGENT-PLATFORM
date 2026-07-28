import { fetchJSON } from "@/lib/api";

import {
  parseProjectSource,
  parseProjectsSource,
  parseTicketSource,
  validateBoardSlug,
  validateProfileName,
  validateTaskId,
  type ProjectSummary,
  type ProjectsWorkspaceRequest,
  type ProjectsWorkspaceView,
} from "./contract";

const KANBAN_API_ROOT = "/api/plugins/kanban";

function safeProfile(profile: string): string | null {
  return profile === "" ? "" : validateProfileName(profile);
}

function query(entries: readonly (readonly [string, string | boolean])[]): string {
  const params = new URLSearchParams();
  for (const [key, value] of entries) params.set(key, String(value));
  return params.toString();
}

function profileEntry(profile: string): readonly (readonly [string, string])[] | null {
  const validated = safeProfile(profile);
  if (validated === null) return null;
  return validated ? [["profile", validated] as const] : [];
}

export function buildProjectsPath(profile: string): string | null {
  const profileParams = profileEntry(profile);
  if (!profileParams) return null;
  return `/agent-platform/projects${profileParams.length ? `?${query(profileParams)}` : ""}`;
}

export function buildProjectPath(boardSlug: string, profile: string): string | null {
  const board = validateBoardSlug(boardSlug);
  const profileParams = profileEntry(profile);
  if (!board || !profileParams) return null;
  const suffix = profileParams.length ? `?${query(profileParams)}` : "";
  return `/agent-platform/projects/${encodeURIComponent(board)}${suffix}`;
}

export function buildTicketPath(boardSlug: string, taskId: string, profile: string): string | null {
  const board = validateBoardSlug(boardSlug);
  const task = validateTaskId(taskId);
  const profileParams = profileEntry(profile);
  if (!board || !task || !profileParams) return null;
  const suffix = profileParams.length ? `?${query(profileParams)}` : "";
  return `/agent-platform/projects/${encodeURIComponent(board)}/tickets/${encodeURIComponent(task)}${suffix}`;
}

export function buildKanbanSourcePath(boardSlug: string, profile: string): string | null {
  const board = validateBoardSlug(boardSlug);
  const profileParams = profileEntry(profile);
  if (!board || !profileParams) return null;
  return `/kanban?${query([["board", board], ...profileParams])}`;
}

export async function listProjectsSource(profile: string): Promise<unknown> {
  const profileParams = profileEntry(profile);
  if (!profileParams) return null;
  return fetchJSON<unknown>(
    `${KANBAN_API_ROOT}/boards?${query([["include_archived", false], ...profileParams])}`,
  );
}

export async function getProjectSource(boardSlug: string, profile: string): Promise<unknown> {
  const board = validateBoardSlug(boardSlug);
  const profileParams = profileEntry(profile);
  if (!board || !profileParams) return null;
  return fetchJSON<unknown>(
    `${KANBAN_API_ROOT}/board?${query([["board", board], ["include_archived", false], ...profileParams])}`,
  );
}

export async function getTicketSource(
  boardSlug: string,
  taskId: string,
  profile: string,
): Promise<unknown> {
  const board = validateBoardSlug(boardSlug);
  const task = validateTaskId(taskId);
  const profileParams = profileEntry(profile);
  if (!board || !task || !profileParams) return null;
  return fetchJSON<unknown>(
    `${KANBAN_API_ROOT}/tasks/${encodeURIComponent(task)}?${query([["board", board], ...profileParams])}`,
  );
}

function isNotFound(error: unknown): boolean {
  return error instanceof Error && error.message.startsWith("404:");
}

async function selectProject(boardSlug: string, profile: string): Promise<ProjectSummary | null> {
  const board = validateBoardSlug(boardSlug);
  if (!board) return null;
  const projects = parseProjectsSource(await listProjectsSource(profile));
  return projects?.find((project) => project.boardSlug === board) ?? null;
}

/**
 * Load one exact source identity. Board/task lookups preflight the board list so
 * missing identities never fall back to Kanban's process-current board.
 */
export async function loadProjectsWorkspaceRequest(
  request: ProjectsWorkspaceRequest,
  profile: string,
): Promise<ProjectsWorkspaceView | null> {
  if (request.kind === "projects") {
    const projects = parseProjectsSource(await listProjectsSource(profile));
    return projects ? Object.freeze({ kind: "projects", projects }) : null;
  }

  try {
    const project = await selectProject(request.boardSlug, profile);
    if (!project) return null;

    if (request.kind === "project") {
      const detail = parseProjectSource(await getProjectSource(project.boardSlug, profile), project);
      return detail ? Object.freeze({ kind: "project", project: detail }) : null;
    }

    const ticket = parseTicketSource(
      await getTicketSource(project.boardSlug, request.taskId, profile),
      project.boardSlug,
    );
    return ticket ? Object.freeze({ kind: "ticket", ticket }) : null;
  } catch (error) {
    if (isNotFound(error)) return null;
    throw error;
  }
}
