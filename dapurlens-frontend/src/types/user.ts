export type Role = "PENGGUNA" | "KREATOR" | "ADMIN";

export interface User {
  id: number;
  email: string;
  name: string;
  role: Role;
  is_active: boolean;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}