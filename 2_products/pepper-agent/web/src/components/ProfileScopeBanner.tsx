import { Users } from "lucide-react";
import { useProfileScope } from "@/contexts/useProfileScope";
import { useI18n } from "@/i18n";

/** Local notice for an explicitly targeted profile-management page. */
export function ProfileScopeBanner() {
  const { profile, currentProfile } = useProfileScope();
  const { t } = useI18n();

  if (!profile || profile === currentProfile) return null;

  return (
    <div className="flex items-center gap-2 border-b border-amber-500/40 bg-amber-500/10 px-4 py-1.5 text-xs text-amber-300">
      <Users className="h-3.5 w-3.5 shrink-0" />
      <span>
        {(
          t.app.managingProfileBanner ??
          "Managing profile “{name}” — config, keys, skills, MCPs and model apply to this profile-local page. Choose new-chat profiles in chat. Pepper governed workflow remains product-global. Profile chats may require their own provider setup."
        ).replace("{name}", profile)}
      </span>
    </div>
  );
}
