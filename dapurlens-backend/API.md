
# DapurLens API Documentation

## Authentication

All authentication endpoints use the `/api/auth` prefix.

### POST /api/auth/register

Register a new user.

**Request body:**
```json
{
  "email": "user@example.com",
  "name": "Example User",
  "password": "your-password"
}
```

**Response:** Returns an access token and user information.

New users receive the default role `PENGGUNA` and are active (`is_active: true`).

### POST /api/auth/login

Authenticate an existing user.

**Request body:**
```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

**Response:**
```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "name": "Example User",
    "role": "PENGGUNA",
    "is_active": true
  }
}
```

### GET /api/auth/me

Get the currently authenticated user's information.

**Authentication:** Bearer token required.

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "Example User",
  "role": "PENGGUNA",
  "is_active": true
}
```

## User Fields

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique user ID |
| `email` | string | User email |
| `name` | string | User display name |
| `role` | string | User role: `PENGGUNA`, `KREATOR`, or `ADMIN` |
| `is_active` | boolean | Indicates whether the account is active |

**Default values:**
- `role`: `PENGGUNA`
- `is_active`: `true`

Passwords and hashed passwords are never included in user response objects.
