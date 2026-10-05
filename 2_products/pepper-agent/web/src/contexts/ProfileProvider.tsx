import { useCallback, useEffect, useMemo, useState, type ReactNode } from "react";
import { useLocation, useSearchParams } from "react-router-dom";
import { api, setManagementProfile } from "@/lib/api";
import { ProfileContext } from "@/contexts/profile-context";
import { isProfileManagementRoute, managementProfileForRoute } from "@/lib/profile-context";

/** Roster plus explicit route-local management scope. Chat owns its binding. */
export function ProfileProvider({ children }: { children: ReactNode }) {
  const [searchParams, setSearchParams] = useSearchParams();
  const { pathname } = useLocation();
  const [profiles, setProfiles] = useState<string[]>([]);
  const [currentProfile, setCurrentProfile] = useState("default");
  const profile = managementProfileForRoute(pathname, searchParams);
  setManagementProfile(profile);

  useEffect(() => {
    // Remove obsolete product-wide links, never propagate profile to another
    // route. Chat's explicit URL is handled by its own session binding.
    if (pathname === "/chat" || isProfileManagementRoute(pathname) || !searchParams.has("profile")) return;
    const next = new URLSearchParams(searchParams);
    next.delete("profile");
    setSearchParams(next, { replace: true });
  }, [pathname, searchParams, setSearchParams]);

  useEffect(() => {
    let cancelled = false;
    Promise.all([api.getProfiles(), api.getActiveProfile()]).then(([roster, info]) => {
      if (cancelled) return;
      setProfiles(roster.profiles.map(p => p.name));
      setCurrentProfile(info.current || "default");
      // Sticky CLI activation is metadata, not a request to rebind this chat.
    }).catch(() => {});
    return () => { cancelled = true; };
  }, []);

  const setProfile = useCallback((name: string) => {
    if (!isProfileManagementRoute(pathname)) return;
    setSearchParams(prev => {
      const next = new URLSearchParams(prev);
      if (name) next.set("profile", name);
      else next.delete("profile");
      return next;
    }, { replace: true });
  }, [pathname, setSearchParams]);

  const value = useMemo(() => ({ profile, currentProfile, profiles, setProfile }), [profile, currentProfile, profiles, setProfile]);
  return <ProfileContext.Provider value={value}>{children}</ProfileContext.Provider>;
}
