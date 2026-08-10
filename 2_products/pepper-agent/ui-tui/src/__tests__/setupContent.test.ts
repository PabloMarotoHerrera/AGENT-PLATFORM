import { afterEach, describe, expect, it, vi } from 'vitest'

import {
  buildSetupRequiredSections,
  isPepperLeadAgentMode,
  setupRequiredTitle
} from '../content/setup.js'

afterEach(() => {
  vi.unstubAllEnvs()
})

describe('setup content', () => {
  it('keeps generic Hermes setup actions outside Pepper mode', () => {
    vi.stubEnv('HERMES_AGENT_PLATFORM_CHAT_MODE', '')

    const sections = buildSetupRequiredSections()
    const rows = sections.flatMap(section => section.rows ?? [])

    expect(isPepperLeadAgentMode()).toBe(false)
    expect(setupRequiredTitle()).toBe('Setup Required')
    expect(rows.map(row => row[0])).toContain('/model')
    expect(rows.map(row => row[0])).toContain('/setup')
  })

  it('uses governed Pepper provider setup content in Pepper mode', () => {
    vi.stubEnv('HERMES_AGENT_PLATFORM_CHAT_MODE', 'pepper-lead-agent')

    const sections = buildSetupRequiredSections()
    const rows = sections.flatMap(section => section.rows ?? [])
    const commands = rows.map(row => row[0])

    expect(isPepperLeadAgentMode()).toBe(true)
    expect(setupRequiredTitle()).toBe('Pepper Provider Required')
    expect(sections[0]?.text).toContain('openai-codex.primary')
    expect(commands).toContain('hermes agent-platform auth add openai-codex.primary')
    expect(commands).not.toContain('hermes auth add openai-codex')
    expect(commands).not.toContain('/model')
    expect(commands).not.toContain('/setup')
  })
})
