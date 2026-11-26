# Changelog

All notable changes to DapurLens are documented in this file.

## [Unreleased]

### Added
- Added `role` column to the users table with default value `PENGGUNA`.
- Added SQL migration `001_add_user_role_and_active.sql`.
- Included `role` and `is_active` in the `UserOut` response schema.
- Added user role and account status to login and current-user API responses.
- Added backend API authentication documentation.
- Enforced database default and NOT NULL constraint on the existing `is_active` column.
- Added unit and API tests for user role, account status, and authentication responses.