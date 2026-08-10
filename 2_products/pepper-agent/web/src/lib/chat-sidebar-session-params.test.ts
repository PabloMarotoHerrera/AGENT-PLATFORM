/**
 * Tests for the dashboard Chat sidebar Pepper authority card.
 */

import { describe, expect, it } from "vitest";
import { createElement } from "react";
import { renderToStaticMarkup } from "react-dom/server";

import { ChatSidebar } from "@/components/ChatSidebar";

describe("ChatSidebar", () => {
  it("renders a read-only Pepper authority card", () => {
    const html = renderToStaticMarkup(createElement(ChatSidebar, { channel: "c1" }));

    expect(html).toContain("Pepper Lead Agent");
    expect(html).toContain("OpenAI Codex OAuth");
    expect(html).toContain("Generic model switching is disabled");
    expect(html).not.toContain("switch model");
  });
});
