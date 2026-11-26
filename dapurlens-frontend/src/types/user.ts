// Peran yang tersimpan di database (akun terdaftar).
export type Role = "PENGGUNA" | "KREATOR" | "ADMIN";

// "GUEST" BUKAN peran di database: itu sebutan untuk pengunjung yang belum
// login (user === null). Dipisah supaya tipe Role tetap persis sama dengan
// yang dikirim backend.
export type ViewerRole = Role | "GUEST";

export interface User {
  id: number;
  email: string;
  name: string;
  role: Role;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}