import { createContext, useContext } from "react";

import type { ProductConfiguration } from "./product-config";

export const ProductConfigurationContext = createContext<ProductConfiguration | null>(null);

export function useProductConfiguration(): ProductConfiguration | null {
  return useContext(ProductConfigurationContext);
}
