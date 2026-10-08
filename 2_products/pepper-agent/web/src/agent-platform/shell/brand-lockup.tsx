import type { ReactNode } from "react";

import type { ProductBrandIdentity } from "../design-system";

export interface ProductBrandLockupProps {
  readonly fallback: ReactNode;
  readonly identity: Readonly<ProductBrandIdentity> | null;
  readonly variant: "mobile" | "sidebar";
}

export function ProductBrandLockup({
  fallback,
  identity,
  variant,
}: ProductBrandLockupProps) {
  if (identity === null) return fallback;

  return (
    <div
      className={`flex min-w-0 items-center gap-2 ${
        variant === "mobile" ? "max-w-[calc(100vw-5rem)]" : "max-w-44"
      }`}
      data-agent-platform-brand-lockup={variant}
    >
      <span
        aria-hidden="true"
        role="presentation"
        className="grid h-8 w-8 shrink-0 place-items-center rounded-lg border text-[0.68rem] font-bold tracking-[0.08em]"
        style={{
          borderColor: "color-mix(in srgb, var(--agent-platform-action-primary) 45%, transparent)",
          background:
            "linear-gradient(135deg, color-mix(in srgb, var(--agent-platform-action-primary) 22%, transparent), color-mix(in srgb, var(--agent-platform-surface-panel) 86%, transparent))",
          color: "var(--agent-platform-action-primary)",
          fontFamily: "var(--agent-platform-font-display)",
        }}
      >
        {identity.lockup.decorativeInitials}
      </span>
      <span className="flex min-w-0 flex-col leading-tight">
        <span
          className={
            variant === "mobile"
              ? "truncate text-[0.95rem] font-bold tracking-[0.05em]"
              : "whitespace-nowrap text-[0.82rem] font-bold tracking-[0.04em]"
          }
          style={{
            color: "var(--agent-platform-text-primary)",
            fontFamily: "var(--agent-platform-font-display)",
          }}
          title={identity.lockup.primaryLabel}
        >
          {identity.lockup.primaryLabel}
        </span>
        {variant === "mobile" ? (
          <span
            className="truncate text-[0.625rem] tracking-[0.06em]"
            style={{ color: "var(--agent-platform-text-muted)" }}
            title={`${identity.lockup.upstreamAttribution} ${identity.upstream.commit}`}
          >
            {identity.lockup.versionLabel} / {identity.lockup.upstreamAttribution} @{" "}
            {identity.upstream.shortCommit}
          </span>
        ) : (
          <span
            className="flex flex-col text-[0.625rem] tracking-[0.05em]"
            style={{ color: "var(--agent-platform-text-muted)" }}
            title={identity.upstream.commit}
          >
            <span>{identity.lockup.versionLabel}</span>
            <span>{identity.lockup.upstreamAttribution}</span>
          </span>
        )}
      </span>
    </div>
  );
}
