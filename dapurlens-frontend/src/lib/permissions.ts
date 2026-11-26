import { Role, User, ViewerRole } from "@/types/user";

// PENTING: fungsi di file ini hanya menentukan apa yang DITAMPILKAN (lencana,
// tombol muncul/sembunyi). Penolakan yang sebenarnya dilakukan backend (403).
// Fungsi lain (canCreateRecipe, canManageRecipe) menyusul di tahap Kreator.

export const ROLE_LABELS: Record<ViewerRole, string> = {
  GUEST: "Tamu",
  PENGGUNA: "Pengguna",
  KREATOR: "Kreator",
  ADMIN: "Admin",
};

export function getViewerRole(user: User | null): ViewerRole {
  return user ? user.role : "GUEST";
}

export function hasRole(user: User | null, ...roles: Role[]): boolean {
  return !!user && roles.includes(user.role);
}