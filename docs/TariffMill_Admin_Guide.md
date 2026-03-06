# TariffMill Administrator Guide

**System Administration, User Management & Deployment**

Version 0.98.0 | Open Source Edition | March 2026

---

## Table of Contents

1. [Overview](#1-overview)
2. [Deployment Options](#2-deployment-options)
3. [First-Time Setup](#3-first-time-setup)
4. [User Management](#4-user-management)
5. [Roles & Permissions](#5-roles--permissions)
6. [Authentication System](#6-authentication-system)
7. [Windows Domain Authentication](#7-windows-domain-authentication)
8. [Admin Panel](#8-admin-panel)
9. [Database Administration](#9-database-administration)
10. [Backup & Recovery](#10-backup--recovery)
11. [Shared Database Setup](#11-shared-database-setup)
12. [Shared Templates Setup](#12-shared-templates-setup)
13. [Auto-Update Configuration](#13-auto-update-configuration)
14. [Building from Source](#14-building-from-source)
15. [Building the Installer](#15-building-the-installer)
16. [Security Considerations](#16-security-considerations)
17. [Troubleshooting](#17-troubleshooting)
18. [Database Schema Reference](#18-database-schema-reference)

---

## 1. Overview

This guide covers administration tasks for TariffMill including user management, authentication configuration, database setup, backups, deployment, and building from source.

**Prerequisites:** Admin role access is required for most operations described here. The first user created via the First-Run Setup Wizard is automatically assigned the admin role.

**Admin Panel Shortcut:** `Ctrl+Shift+A` opens the Admin Panel from anywhere in the application.

---

## 2. Deployment Options

### Standard Installer

The Windows installer (`TariffMill_Setup_x.xx.x.exe`) provides Start Menu/Desktop shortcuts, shared `auth_users.json`, and an uninstaller. Default path: `C:\Program Files\TariffMill\`

### Portable Executable

Single file, no installation required. Stores database locally alongside the executable. Ideal for USB or restricted environments.

### Multi-User (Shared Network Database)

1. Install TariffMill on each workstation
2. Place `tariffmill.db` on a network drive
3. Configure each installation's `config.ini` to point to the shared path
4. Set up `auth_users.json` or Windows domain authentication

See [Shared Database Setup](#11-shared-database-setup) for details.

### pip Install (Linux/macOS)

```bash
pip install git+https://github.com/ProcessLogicLabs/open-tariffmill.git
```

---

## 3. First-Time Setup

### First-Run Setup Wizard

When no user accounts exist, the wizard collects:

| Field | Validation |
|-------|-----------|
| **Name** | Required |
| **Email** | Required, must contain `@` |
| **Password** | Required, minimum 6 characters |
| **Confirm Password** | Must match |

A SHA-256 password hash is generated with a random 16-byte salt. The user is saved with role `admin`.

### Triggering the Wizard Again

Edit `auth_users.json` to have empty users and restart:

```json
{
    "_comment": "TariffMill User Authentication",
    "users": {}
}
```

### Pre-configuring Users

Use `scripts/generate_password_hash.py` or:

```python
from Tariffmill.tariffmill import AuthenticationManager
result = AuthenticationManager.generate_password_hash("your_password")
print(result)  # {'password_hash': '...', 'salt': '...'}
```

---

## 4. User Management

### Accessing User Management

Press `Ctrl+Shift+A` > **User Management** tab.

### User List Table

| Column | Description |
|--------|-------------|
| Email/Username | Login identifier |
| Name | Display name |
| Role | admin (green), division_admin (blue), user |
| Status | Active (green) or Suspended (red) |
| AI Assistant | Checkbox — always on for admins |

### Adding a User

Click **Add User**. Two user types:

**Email/Password User:** Email (must contain `@`), name, role, password, confirm password.

**Windows Domain User:** Username (lowercase), domain (pre-filled from allowed domains), name, role. Stored as `DOMAIN\username` with `auth_type: "windows"`.

### Editing a User

Select user, click **Edit User**. Can change: name, role, managed divisions, default division. Cannot change email/username.

### Resetting a Password

Select user, click **Reset Password**. Enter new password and confirm. Hash and salt are regenerated.

### Suspending / Activating

Click **Suspend/Activate** to toggle. Suspended users cannot log in and see: *"Your account has been suspended."*

### Deleting a User

Click **Delete User**. Permanent and irreversible. Ensure at least one admin remains.

### AI Assistant Access

The **AI Assistant** checkbox controls access to the AI Templates tab.

- **Admin users:** Always have access (checkbox disabled, checked)
- **Other users:** Off by default; toggle to grant or revoke

> **Important — Cost and Risk Considerations:**
>
> The AI Template Generator makes API calls to external AI services (Anthropic Claude, OpenAI, etc.) that **charge per use**. Every user with AI Assistant access can incur costs against the configured API key. Before granting access, ensure users understand that:
>
> - API calls are billed to the API key configured in Settings > AI Provider
> - Costs can accumulate quickly during extended template development sessions
> - TariffMill does not impose usage limits or spending caps
> - This feature has not been extensively tested and is provided as-is
> - AI-generated templates may require manual review and debugging before production use
>
> Consider limiting AI Assistant access to users who need to create new templates and who understand the associated costs.

---

## 5. Roles & Permissions

| Capability | user | division_admin | admin |
|-----------|------|----------------|-------|
| Process invoices | Yes | Yes | Yes |
| View/edit parts database | Yes | Yes | Yes |
| Search HTS database | Yes | Yes | Yes |
| Use PDF processing | Yes | Yes | Yes |
| Manage own folder profiles | Yes | Yes | Yes |
| Manage division users | No | Own divisions | All |
| Access Admin Panel (Ctrl+Shift+A) | No | No | Yes |
| Manage all users | No | No | Yes |
| View audit logs | No | No | Yes |
| Configure system settings | No | No | Yes |
| AI Assistant access | If granted | If granted | Always |

---

## 6. Authentication System

### Password Authentication

- Passwords hashed with **SHA-256** using random 16-byte hex salt
- Formula: `SHA256(salt + password)`
- Both hash and salt stored in `auth_users.json`
- Cached credentials enable offline authentication

### auth_users.json Format

```json
{
    "users": {
        "admin@example.com": {
            "password_hash": "a1b2c3...",
            "salt": "0123456789abcdef...",
            "role": "admin",
            "name": "Admin User",
            "auth_type": "password"
        },
        "MYDOMAIN\\jsmith": {
            "role": "user",
            "name": "John Smith",
            "auth_type": "windows"
        }
    }
}
```

### Authentication Flow

```
1. Load auth_users.json
2. No users exist? -> First-Run Setup Wizard
3. Users exist? -> Try Windows domain auto-login
   a. Domain in allowed list + user found -> Auto-login
   b. Domain in allowed list + user NOT found -> Auto-provision as 'user' role, then auto-login
   c. Domain not allowed or not on domain -> Show Login Dialog
4. Login Dialog -> Verify password hash -> Grant access with role
```

### File Search Locations (Priority Order)

1. Application data directory (`BASE_DIR/auth_users.json`)
2. Home config repo (`~/TariffMill_Config/auth_users.json`)
3. Installation directory (`INSTALL_DIR/auth_users.json`)
4. Project root (development)
5. Script directory (development)

---

## 7. Windows Domain Authentication

### How It Works

Windows domain authentication uses the `USERDOMAIN` and `USERNAME` environment variables provided by the Windows operating system. When a user is logged into a domain that TariffMill trusts, they are authenticated automatically — no password prompt, no login dialog.

**New domain users are auto-provisioned:** When a user on an allowed domain launches TariffMill for the first time, their account is created automatically with the "user" role. The admin can then adjust roles, grant AI access, or suspend accounts as needed from the Admin Panel.

### Configuration

**Step 1:** Set allowed domains in the Admin Panel (`Ctrl+Shift+A`) > Settings, or via:

```python
set_app_setting('allowed_domains', 'CORPORATE,BRANCH_OFFICE')
```

Comma-separated, case-insensitive. Example: `MYCORP,BRANCH1,BRANCH2`

**Step 2:** That's it. Any user on an allowed domain will auto-login on next launch.

### What Happens on First Login

1. User launches TariffMill on a machine joined to `MYCORP` domain
2. TariffMill reads `USERDOMAIN=MYCORP` and `USERNAME=jsmith` from the OS
3. Checks if `MYCORP` is in the allowed domains list
4. User `MYCORP\jsmith` not found in user list → **auto-provisions** with role `user`
5. Saves new entry to `auth_users.json`
6. User is logged in automatically

### Auto-Provisioned User Entry

Auto-provisioned users are saved with the following data:

```json
{
    "MYCORP\\jsmith": {
        "role": "user",
        "name": "Jsmith",
        "auth_type": "windows",
        "auto_provisioned": true,
        "created": "2026-03-06T12:00:00"
    }
}
```

### Managing Domain Users

After auto-provisioning, admins can:
- **Promote** a user to `admin` or `division_admin` via the User Management tab
- **Grant AI access** by checking the AI Assistant checkbox
- **Suspend** a user to block future logins (they see "Your account has been suspended")
- **Pre-create** users manually via Add User > Windows Domain User if you want to assign roles before their first login

---

## 8. Admin Panel

Open with `Ctrl+Shift+A` (admin role required). Four tabs:

### Audit Log Tab

Tracks all export attempts. Filter by event type (Successful, Blocked, etc.) and date range (1-365 days). Shows date, time, event, file number, file name, lines, value, user, and info. Limited to 500 most recent entries.

### System Info Tab

Displays application version, current user, machine name, platform, Python version, database path, output directory, parts count, and audit log entry count.

### User Statistics Tab

- **TariffMill totals:** Parts count, total exports, total line items, active users
- **PDF Processing totals:** PDFs processed, items extracted, success rate, templates used
- **Exports by user table:** Entry writer, total exports, line items, last export
- **PDF processing by user table:** User, PDFs processed, successful/failed, items extracted, avg confidence
- **Recent daily activity** (last 30 days)

### User Management Tab

See [User Management](#4-user-management).

---

## 9. Database Administration

### Database Location

Configurable via `config.ini`:

```ini
[database]
windows_path = Y:\Shared\TariffMill\tariffmill.db
linux_path = /mnt/shared/tariffmill/tariffmill.db
```

Default: `Tariffmill/Resources/tariffmill.db`

### Database Tables

| Table | Purpose |
|-------|---------|
| `parts_master` | Parts inventory with HTS codes and material data |
| `tariff_232` | Section 232 tariff classifications |
| `sec_232_actions` | Chapter 99 action codes |
| `mapping_profiles` | Invoice column mapping profiles |
| `output_column_mappings` | Export format profiles |
| `folder_profiles` | Input/output folder profiles (per-user) |
| `mid_table` | Manufacturer IDs |
| `hts_units` | HTS quantity unit cache |
| `app_config` | Application configuration key-value store |
| `export_audit_log` | Export activity audit trail |
| `file_number_divisions` | Division-based file number patterns |

### Automatic Migrations

- **billing_settings -> app_config:** Migrates `allowed_domains` and `shared_templates_folder`, drops billing tables
- **folder_profiles per-user:** Adds `created_by` column for per-user profiles
- **parts_master created_date:** Adds column and seeds from `last_updated`

All migrations are non-destructive and idempotent.

---

## 10. Backup & Recovery

### Backup Configuration

In Settings > Database page, or `config.ini`:

```ini
[backup]
enabled = true
folder = Y:\Backups\TariffMill
schedule = daily
keep_count = 7
backup_machine = SERVER01
backup_time = 02:00
```

| Setting | Options | Default |
|---------|---------|---------|
| `enabled` | true/false | false |
| `folder` | Path | (empty) |
| `schedule` | daily, weekly, startup | daily |
| `keep_count` | 1-100 | 7 |
| `backup_machine` | Hostname | (empty) |
| `backup_time` | HH:MM (24h) | 02:00 |

Backup files: `tariffmill_backup_YYYYMMDD_HHMMSS.db`. Old backups beyond `keep_count` are auto-deleted.

### Recovery

1. Close TariffMill on all machines
2. Replace `tariffmill.db` with the backup file
3. Restart TariffMill

---

## 11. Shared Database Setup

1. Place `tariffmill.db` on a network drive (e.g., `Y:\Shared\TariffMill\`)
2. Configure `config.ini` on each workstation with `windows_path`
3. First user to launch creates all tables automatically
4. Set up `auth_users.json` or Windows domain auth

**Per-user vs shared:**

| Type | Storage | Scope |
|------|---------|-------|
| Theme, font, window geometry | Windows Registry | Per user |
| Folder profiles | SQLite (with `created_by`) | Per user |
| Parts, MIDs, HTS, profiles | SQLite | Shared |
| Audit log | SQLite | Shared |

---

## 12. Shared Templates Setup

1. Set **Shared Templates Folder** in Settings > Templates to a network path
2. Place `.py` template files in the folder
3. All users pick them up on next restart

Templates with the same filename as bundled templates are skipped (bundled takes priority).

---

## 13. Auto-Update Configuration

Updates check the GitHub Releases API. Version filtering ensures open-source edition (0.x.x) only sees 0.x.x releases.

| Setting | Default |
|---------|---------|
| Check for updates on startup | On |
| Install updates silently | On |

Silent mode uses: `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS`

To disable: uncheck in Settings > Updates, or block `api.github.com` at the firewall.

---

## 14. Building from Source

```bash
git clone https://github.com/ProcessLogicLabs/open-tariffmill.git
cd open-tariffmill
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller
cd Tariffmill
pyinstaller TariffMill.spec
```

Output: `dist/TariffMill/TariffMill.exe`

---

## 15. Building the Installer

Requires [Inno Setup 6](https://jrsoftware.org/isinfo.php):

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" tariffmill_setup.iss
```

Output: `installer_output/TariffMill_Setup_0.98.0.exe`

---

## 16. Security Considerations

### Passwords

SHA-256 with random 16-byte salt. Never stored in plain text.

### auth_users.json

Contains hashed passwords only. Set file permissions: read for all users, write for admins.

### Network Database

SQLite has no built-in auth — use NTFS permissions to restrict access.

### API Keys

AI API keys stored locally, sent only to the configured provider. Not shared across users.

### Audit Trail

All export attempts logged in `export_audit_log` with user identity, machine ID, timestamp, and success/failure. Logs cannot be deleted through the UI.

### Data Privacy

- No telemetry or analytics
- Invoice data passes through transiently
- Network calls limited to: GitHub API (optional update checks) and AI API (optional template generation)

---

## 17. Troubleshooting

### Authentication Issues

| Problem | Solution |
|---------|----------|
| First-run wizard doesn't appear | Clear `users` in auth_users.json |
| "Account suspended" | Admin unsuspends via Admin Panel |
| Windows auto-login fails | Verify domain is in allowed_domains (Admin Panel > Settings). Users are auto-provisioned — no manual user entry needed. Check logs for details. |
| Empty user list | Place auth_users.json in installation directory |

### Database Issues

| Problem | Solution |
|---------|----------|
| "Database is locked" | Close other TariffMill instances |
| Parts table empty after upgrade | Verify config.ini database path |
| Slow with shared DB | Move to faster storage or use local copy |

### Log Files

**Help** > **View Log** for authentication, database, template, and processing details.

---

## 18. Database Schema Reference

### parts_master

```sql
CREATE TABLE parts_master (
    part_number TEXT PRIMARY KEY,
    description TEXT, hts_code TEXT, country_origin TEXT,
    mid TEXT, client_code TEXT,
    steel_pct REAL DEFAULT 0.0, non_steel_pct REAL DEFAULT 0.0,
    aluminum_pct REAL DEFAULT 0.0, copper_pct REAL DEFAULT 0.0,
    wood_pct REAL DEFAULT 0.0, auto_pct REAL DEFAULT 0.0,
    country_of_melt TEXT, country_of_cast TEXT, country_of_smelt TEXT,
    Sec301_Exclusion_Tariff TEXT, qty_unit TEXT, hts_verified TEXT,
    created_date TEXT, last_updated TEXT
)
```

### app_config

```sql
CREATE TABLE app_config (key TEXT PRIMARY KEY, value TEXT)
```

Common keys: `allowed_domains`, `shared_templates_folder`, `last_auth_user`, `last_auth_time`, `cached_auth_users`

### export_audit_log

```sql
CREATE TABLE export_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT, event_date TEXT, event_time TEXT,
    file_number TEXT, file_name TEXT, line_count INTEGER,
    total_value REAL, user_name TEXT, machine_id TEXT,
    ip_address TEXT, success INTEGER DEFAULT 1,
    failure_reason TEXT, billing_recorded INTEGER DEFAULT 0,
    additional_info TEXT
)
```

### folder_profiles

```sql
CREATE TABLE folder_profiles (
    profile_name TEXT NOT NULL, created_by TEXT NOT NULL DEFAULT '',
    input_folder TEXT, output_folder TEXT, created_date TEXT,
    PRIMARY KEY (profile_name, created_by)
)
```

### Other Tables

- **tariff_232**: hts_code (PK), material, classification, chapter, ch99/rate columns by country
- **sec_232_actions**: tariff_no (PK), action, description, rates, dates, declarations
- **mapping_profiles**: profile_name (PK), mapping_json, header_row
- **output_column_mappings**: profile_name (PK), mapping_json
- **mid_table**: mid (PK), manufacturer_name, customer_id, related_parties
- **hts_units**: hts_code (PK), qty_unit
- **profile_links**: input_profile_name (PK) -> export_profile_name
- **file_number_divisions**: id (PK), division_name, prefix, total_length, is_active

---

*TariffMill — Professional Customs Documentation Processing*

*Open Source Edition — MIT License*

*Copyright (c) 2024-2026 Process Logic Labs, LLC*
