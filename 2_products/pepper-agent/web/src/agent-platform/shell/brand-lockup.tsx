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
      className={`flex min-w-0 flex-col leading-tight ${
        variant === "mobile" ? "max-w-[calc(100vw-5rem)]" : "max-w-40"
      }`}
      data-agent-platform-brand-lockup={variant}
    >
      <span
        className={
          variant === "mobile"
            ? "truncate text-[0.95rem] font-bold tracking-[0.05em] text-midground"
            : "whitespace-nowrap text-[0.8rem] font-bold tracking-[0.04em] text-midground"
        }
        style={{ fontFamily: "var(--agent-platform-font-display)" }}
        title={identity.product.displayName}
      >
        {identity.product.displayName}
      </span>
      {variant === "mobile" ? (
        <span
          className="truncate text-[0.625rem] tracking-[0.06em]"
          style={{ color: "var(--agent-platform-text-muted)" }}
          title={`${identity.upstream.displayName} ${identity.upstream.version} ${identity.upstream.commit}`}
        >
          {identity.product.version} / {identity.upstream.displayName}{" "}
          {identity.upstream.version} @ {identity.upstream.shortCommit}
        </span>
      ) : (
        <span
          className="flex flex-col text-[0.625rem] tracking-[0.05em]"
          style={{ color: "var(--agent-platform-text-muted)" }}
          title={identity.upstream.commit}
        >
          <span>{identity.product.version}</span>
          <span>
            {identity.upstream.displayName} {identity.upstream.version}
          </span>
        </span>
      )}
    </div>
  );
}
