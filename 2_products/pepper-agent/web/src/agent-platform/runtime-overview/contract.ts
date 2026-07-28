export type RuntimeGatewayState =
  | "off"
  | "running"
  | "starting"
  | "stopped"
  | "failed"
  | "unknown";

export interface RuntimeOverviewSnapshot {
  readonly platform: Readonly<{
    version: string;
    releaseDate: string;
    configVersion: number;
    latestConfigVersion: number;
    updateAvailable: boolean;
  }>;
  readonly gateway: Readonly<{
    state: RuntimeGatewayState;
    running: boolean;
    busy: boolean;
    drainable: boolean;
  }>;
  readonly activity: Readonly<{
    activeSessions: number;
    activeAgents: number;
  }>;
  readonly access: Readonly<{
    authRequired: boolean;
  }>;
}

function asRecord(value: unknown): Record<string, unknown> | null {
  return value !== null && typeof value === "object" && !Array.isArray(value)
    ? value as Record<string, unknown>
    : null;
}

function asBoundedString(value: unknown, maxLength: number): string | null {
  if (typeof value !== "string") return null;
  const normalized = value.trim();
  return normalized.length > 0 && normalized.length <= maxLength ? normalized : null;
}

function asNonNegativeInteger(value: unknown): number | null {
  return typeof value === "number" && Number.isSafeInteger(value) && value >= 0
    ? value
    : null;
}

function asBoolean(value: unknown): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function normalizeGatewayState(value: unknown, running: boolean): RuntimeGatewayState {
  if (value === "running") return "running";
  if (value === "starting") return "starting";
  if (value === "stopped") return "stopped";
  if (value === "startup_failed") return "failed";
  if (value === null && !running) return "off";
  return running ? "running" : "unknown";
}

/** Project the public status response into the only fields this surface retains. */
export function parseRuntimeOverviewSnapshot(value: unknown): RuntimeOverviewSnapshot | null {
  const source = asRecord(value);
  if (!source) return null;

  const version = asBoundedString(source.version, 64);
  const releaseDate = asBoundedString(source.release_date, 32);
  const configVersion = asNonNegativeInteger(source.config_version);
  const latestConfigVersion = asNonNegativeInteger(source.latest_config_version);
  const canUpdateHermes = asBoolean(source.can_update_hermes);
  const gatewayRunning = asBoolean(source.gateway_running);
  const gatewayBusy = asBoolean(source.gateway_busy);
  const gatewayDrainable = asBoolean(source.gateway_drainable);
  const activeSessions = asNonNegativeInteger(source.active_sessions);
  const activeAgents = asNonNegativeInteger(source.active_agents);
  const authRequired = asBoolean(source.auth_required);

  if (
    version === null ||
    releaseDate === null ||
    configVersion === null ||
    latestConfigVersion === null ||
    canUpdateHermes === null ||
    gatewayRunning === null ||
    gatewayBusy === null ||
    gatewayDrainable === null ||
    activeSessions === null ||
    activeAgents === null ||
    authRequired === null
  ) {
    return null;
  }

  return Object.freeze({
    platform: Object.freeze({
      version,
      releaseDate,
      configVersion,
      latestConfigVersion,
      updateAvailable: canUpdateHermes && latestConfigVersion > configVersion,
    }),
    gateway: Object.freeze({
      state: normalizeGatewayState(source.gateway_state, gatewayRunning),
      running: gatewayRunning,
      busy: gatewayBusy,
      drainable: gatewayDrainable,
    }),
    activity: Object.freeze({ activeSessions, activeAgents }),
    access: Object.freeze({ authRequired }),
  });
}
