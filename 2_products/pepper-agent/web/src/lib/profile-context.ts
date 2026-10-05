/** Profiles are local request/session identities, never product identities. */
const MANAGEMENT_ROUTES = ["/config", "/env", "/models", "/skills", "/mcp", "/sessions", "/profiles"];

export function isProfileManagementRoute(pathname: string): boolean {
  return MANAGEMENT_ROUTES.some(path => pathname === path || pathname.startsWith(`${path}/`));
}

export function managementProfileForRoute(pathname: string, params: URLSearchParams): string {
  return isProfileManagementRoute(pathname) ? params.get("profile") ?? "" : "";
}

export function profileDisplayName(profile: string): string {
  if (!profile) return "Pepper Default";
  if (profile === "pepper-architecture-product") return "Architecture";
  if (profile === "pepper-implementation-product") return "Implementation";
  return profile;
}

export interface ChatProfileBinding {
  readonly profile: string;
  readonly resume: string | null;
}

export function newChatBinding(profile: string): ChatProfileBinding {
  return Object.freeze({ profile, resume: null });
}

export function chatBindingFromUrl(params: URLSearchParams): ChatProfileBinding {
  // Preserve even unknown values: backend validation must reject them rather
  // than silently resuming the same session ID in the default profile.
  return Object.freeze({ profile: params.get("profile") ?? "", resume: params.get("resume") });
}

export function resolveChatBinding(bound: ChatProfileBinding, params: URLSearchParams, active: boolean): ChatProfileBinding {
  if (!active || (!params.has("profile") && !params.has("resume"))) return bound;
  const incoming = chatBindingFromUrl(params);
  return incoming.profile === bound.profile && incoming.resume === bound.resume ? bound : incoming;
}

export interface ChatLocationBinding {
  readonly binding: ChatProfileBinding;
  readonly locationKey: string | null;
}

/** Consume each navigation once. A pending new-chat binding wins over the old URL. */
export function consumeChatLocation(state: ChatLocationBinding, params: URLSearchParams, active: boolean, locationKey: string): ChatLocationBinding {
  if (!active || state.locationKey === locationKey) return state;
  return { binding: resolveChatBinding(state.binding, params, true), locationKey };
}

export function chatBindingParams(binding: ChatProfileBinding): URLSearchParams {
  const params = new URLSearchParams();
  if (binding.profile) params.set("profile", binding.profile);
  if (binding.resume) params.set("resume", binding.resume);
  return params;
}

export function chatSessionPath(profile: string, resume: string | null = null, learn?: string): string {
  const params = chatBindingParams({ profile, resume });
  // Explicit empty default is meaningful when opening a new chat from another
  // local surface while a named-profile PTY is already mounted.
  params.set("profile", profile);
  if (learn) params.set("learn", learn);
  return `/chat?${params}`;
}
