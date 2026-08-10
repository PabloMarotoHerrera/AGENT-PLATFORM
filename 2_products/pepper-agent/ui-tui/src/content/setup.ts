import type { PanelSection } from '../types.js'

export const SETUP_REQUIRED_TITLE = 'Setup Required'
export const PEPPER_SETUP_REQUIRED_TITLE = 'Pepper Provider Required'

export const isPepperLeadAgentMode = (): boolean => {
  const value = (process.env.HERMES_AGENT_PLATFORM_CHAT_MODE ?? '')
    .trim()
    .toLowerCase()
    .replace(/_/g, '-')

  return value === 'pepper-lead-agent' || value === 'pepper-lead' || value === 'pepper'
}

export const setupRequiredTitle = (): string =>
  isPepperLeadAgentMode() ? PEPPER_SETUP_REQUIRED_TITLE : SETUP_REQUIRED_TITLE

export const buildSetupRequiredSections = (): PanelSection[] => {
  if (isPepperLeadAgentMode()) {
    return [
      {
        text:
          'Pepper Lead Agent provider unavailable: governed credential profile openai-codex.primary is required before this chat can start a session.'
      },
      {
        rows: [
          [
            'hermes agent-platform auth add openai-codex.primary',
            'provision openai-codex.primary in the governed store'
          ],
          ['Refresh /chat', 'start Pepper Lead Agent after authentication'],
          ['Ctrl+C', 'exit this chat process']
        ],
        title: 'Actions'
      }
    ]
  }

  return [
    {
      text: 'Hermes needs a model provider before the TUI can start a session.'
    },
    {
      rows: [
        ['/model', 'configure provider + model in-place'],
        ['/setup', 'run full first-time setup wizard in-place'],
        ['Ctrl+C', 'exit and run `hermes setup` manually']
      ],
      title: 'Actions'
    }
  ]
}
