import type { ReactNode } from "react";

import { ProductConfigurationContext } from "./product-config-context";
import type { ProductConfiguration } from "./product-config";

interface ProductConfigurationProviderProps {
  children: ReactNode;
  value: ProductConfiguration | null;
}

export function ProductConfigurationProvider({
  children,
  value,
}: ProductConfigurationProviderProps) {
  return (
    <ProductConfigurationContext.Provider value={value}>
      {children}
    </ProductConfigurationContext.Provider>
  );
}
