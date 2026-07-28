import { FolderKanban } from "lucide-react";

import type { ProductExtensionDescriptor } from "../extensions";
import { ProjectDetailPage } from "./project-detail-page";
import { ProjectsPage } from "./projects-page";
import { TicketDetailPage } from "./ticket-detail-page";

export const PROJECTS_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.projects",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/projects",
    component: ProjectsPage,
    title: "Projects",
  }),
  navigation: Object.freeze({
    groupId: "agent-platform",
    label: "Projects",
    icon: FolderKanban,
    placement: Object.freeze({ kind: "end" }),
  }),
});

export const PROJECT_DETAIL_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.project_detail",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/projects/:boardSlug",
    component: ProjectDetailPage,
    title: "Project",
  }),
});

export const TICKET_DETAIL_DESCRIPTOR: ProductExtensionDescriptor = Object.freeze({
  id: "agent_platform.ui.ticket_detail",
  owner: "AGENT_PLATFORM",
  featureId: "agent_platform.product_ui",
  visibleWhenExperimental: true,
  route: Object.freeze({
    path: "/agent-platform/projects/:boardSlug/tickets/:taskId",
    component: TicketDetailPage,
    title: "Ticket",
  }),
});

export const PROJECTS_TICKETS_DESCRIPTORS: readonly ProductExtensionDescriptor[] = Object.freeze([
  PROJECTS_DESCRIPTOR,
  PROJECT_DETAIL_DESCRIPTOR,
  TICKET_DETAIL_DESCRIPTOR,
]);
