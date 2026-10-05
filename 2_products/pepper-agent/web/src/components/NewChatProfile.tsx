import { profileDisplayName } from "@/lib/profile-context";

interface NewChatProfileProps {
  readonly profiles: readonly string[];
  readonly currentProfile: string;
  readonly draft: string;
  readonly boundProfile: string;
  readonly onChange: (profile: string) => void;
  readonly onStart: () => void;
}

/** Selecting a draft never changes the running PTY or any management page. */
export function NewChatProfile({ profiles, currentProfile, draft, boundProfile, onChange, onStart }: NewChatProfileProps) {
  return <section aria-label="New chat" className="flex flex-wrap items-center gap-2 text-sm">
    <label htmlFor="new-chat-profile">New chat profile</label>
    <select id="new-chat-profile" value={draft} onChange={event => onChange(event.target.value)} className="rounded border border-current/20 bg-background px-2 py-1">
      <option value="">Pepper Default</option>
      {profiles.filter(name => name !== currentProfile).map(name => <option key={name} value={name}>{profileDisplayName(name)}</option>)}
    </select>
    <button type="button" onClick={onStart} className="rounded border border-current/20 px-3 py-1">New chat</button>
    <span title={boundProfile || currentProfile}>Session profile: {profileDisplayName(boundProfile)}</span>
    <p className="basis-full text-xs text-text-secondary">Profile applies to the new chat, its history and provider setup. Pepper governed workflow remains product-global.</p>
  </section>;
}
