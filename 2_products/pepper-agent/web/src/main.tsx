import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import App from "./App";
import { SystemActionsProvider } from "./contexts/SystemActions";
import { I18nProvider } from "./i18n";
import { exposePluginSDK } from "./plugins";
import { ThemeProvider } from "./themes";
import { HERMES_BASE_PATH } from "./lib/api";
import { loadProductConfiguration } from "./agent-platform/product-config";
import { ProductConfigurationProvider } from "./agent-platform/product-config-provider";

// Expose the plugin SDK before rendering so plugins loaded via <script>
// can access React, components, etc. immediately.
exposePluginSDK();

async function mountDashboard() {
  const productConfiguration = await loadProductConfiguration();

  createRoot(document.getElementById("root")!).render(
    <BrowserRouter basename={HERMES_BASE_PATH || undefined}>
      <I18nProvider>
        <ThemeProvider>
          <SystemActionsProvider>
            <ProductConfigurationProvider value={productConfiguration}>
              <App />
            </ProductConfigurationProvider>
          </SystemActionsProvider>
        </ThemeProvider>
      </I18nProvider>
    </BrowserRouter>,
  );
}

void mountDashboard();
