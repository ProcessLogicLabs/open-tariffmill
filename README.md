# TariffMill — Open Source Edition

**Professional Customs Documentation Processing System**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.98.0-green.svg)](Tariffmill/version.py)

TariffMill is a free, open-source desktop application for import/export businesses, customs brokers, and trade compliance professionals. It automates invoice processing, manages parts databases, and ensures compliance with U.S. Section 232 and Section 301 tariff requirements.

---

## Key Features

### Invoice Processing
- Process commercial invoices (CSV, XLSX formats)
- Generate CBP-compliant upload worksheets for e2Open and other customs management systems
- Automatic Section 232 derivative line creation with prorated values
- Preview and edit data before export with color-coded material rows
- Split exports by invoice number

### PDF Processing (OCRMill)
- AI-powered PDF invoice extraction using customizable templates
- Drag-and-drop PDF processing
- Batch processing and folder monitoring (auto-process new files)
- Template matching by supplier with confidence scoring
- Editable results before sending to invoice processing

### Parts Master Database
- Maintain comprehensive parts inventory with HTS codes
- Track country of origin, melt, cast, and smelt locations
- Store material ratios (steel, aluminum, copper, wood, automotive)
- Import parts from CSV/Excel files
- Advanced search with quick presets, field search, and custom SQL

### Tariff Compliance
- **Section 232**: Automatic tracking of steel, aluminum, copper, wood, and automotive tariffs with derivative line splitting
- **Section 301**: Identify products with exclusion tariffs and expiration tracking
- Color-coded indicators for quick material identification
- Declaration codes (07/08) auto-assigned with melt/cast/smelt country codes

### Multi-User Authentication
- First-run setup wizard creates your admin account on fresh installs
- Role-based access control (admin, division_admin, user)
- Windows domain auto-login with automatic user provisioning — any user on an allowed domain is logged in automatically and added to the user list
- Admin panel for user management, audit logs, and statistics

### HTS Database Reference
- Built-in searchable HTS database
- Quick lookup of tariff codes and descriptions
- CBP quantity unit information

### Flexible Configuration
- Save and reuse invoice mapping profiles for different suppliers
- Customizable output column mapping and export profiles
- Per-user folder profiles for input/output directories
- 7 theme options (System Default, Fusion Light/Dark, Ocean, Light Cyan, Muted Cyan, macOS)
- Configurable database backups with retention policies

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Windows 10 | Windows 11 |
| RAM | 4 GB | 8 GB |
| Disk | 200 MB | 500 MB |
| Display | 1280 x 720 | 1920 x 1080 |

Linux and macOS are supported via pip installation.

---

## Installation

### Windows Installer (Recommended)

Download `TariffMill_Setup_x.xx.x.exe` from the [Releases](https://github.com/ProcessLogicLabs/open-tariffmill/releases) page and run the installer.

### Windows Portable

Download `TariffMill.exe` from the [Releases](https://github.com/ProcessLogicLabs/open-tariffmill/releases) page. No installation required — just run the executable.

#### Windows SmartScreen Warning

On first run, Windows may show a "Windows protected your PC" warning. This is normal for newly distributed software:

1. Click **"More info"**
2. Click **"Run anyway"**

### Linux / macOS (pip)

```bash
pip install git+https://github.com/ProcessLogicLabs/open-tariffmill.git
tariffmill
```

### From Source

```bash
git clone https://github.com/ProcessLogicLabs/open-tariffmill.git
cd open-tariffmill
python -m venv venv
.\venv\Scripts\activate         # Windows
source venv/bin/activate        # Linux/macOS
pip install -r requirements.txt
python Tariffmill/tariffmill.py
```

---

## Getting Started

### First Launch

On the first launch with no existing users, TariffMill presents a **First-Run Setup Wizard** to create your admin account. Enter your name, email, and password — then log in.

### Basic Workflow

1. **Configure Folders** — Go to Settings > Settings... to set input/output directories, or create a folder profile
2. **Load Invoice** — Select a CSV or XLSX invoice file from the input files list
3. **Map Columns** — Create or select a mapping profile for the invoice format
4. **Enter Values** — Set commercial invoice total, net weight, MID, and file number
5. **Process** — Click "Process Invoice" to match parts and apply tariff data
6. **Review** — Check the preview table with color-coded material rows
7. **Export** — Click "Export Worksheet" to generate the final upload file

### Parts Database

- **Import**: Master Data > Master Data... > Parts Import tab for bulk CSV/Excel import
- **Search**: Quick search presets (Missing HTS, Steel Parts, etc.) or custom SQL queries
- **Edit**: Double-click any cell in the Parts View tab to modify
- **Verify**: Click "Verify HTS" to validate codes against the reference database

### Output Mapping

Customize which columns appear in your export:
1. Go to Master Data > Master Data... > Output Mapping tab
2. Check/uncheck columns to include or exclude
3. Drag columns to reorder
4. Save as a profile for reuse

---

## File Structure

```
open-tariffmill/
├── Tariffmill/
│   ├── tariffmill.py              # Main application
│   ├── version.py                 # Version management
│   ├── auto_update.py             # Auto-update system
│   ├── settings_dialog.py         # Settings UI
│   ├── settings_manager.py        # Settings persistence
│   ├── auth_users.json            # User credentials (hashed)
│   ├── templates/                 # PDF extraction templates
│   │   ├── base_template.py       # Base class for templates
│   │   └── sample_template.py     # Example template
│   └── Resources/
│       ├── tariffmill.db          # SQLite database
│       └── References/
│           ├── hts.db             # HTS tariff database
│           └── htsdata.json       # HTS reference data
├── docs/
│   ├── TariffMill_User_Guide.md   # Full user guide
│   ├── TariffMill_Admin_Guide.md  # Administration guide
│   ├── AUTO_UPDATE_GUIDE.md       # Auto-update documentation
│   └── flowcharts/                # Architecture & workflow diagrams
├── scripts/
│   └── generate_password_hash.py  # Password hash utility
├── pyproject.toml                 # Python package configuration
├── requirements.txt               # Python dependencies
├── tariffmill_setup.iss           # Inno Setup installer script
└── LICENSE                        # MIT License
```

---

## Configuration

Settings are stored in three locations:

| Location | What's Stored | Scope |
|----------|--------------|-------|
| **SQLite database** (`app_config` table) | Shared settings, allowed domains, template paths | All users |
| **Windows Registry** (`HKCU\Software\TariffMill`) | Theme, font size, window geometry, column widths | Per user |
| **auth_users.json** | User accounts with hashed passwords, roles | All users |

---

## Technology Stack

- **Python 3.12** — Core language
- **PyQt5** — Desktop GUI framework
- **Pandas** — Data processing and transformation
- **SQLite** — Local/shared database
- **OpenPyXL** — Excel file reading and writing
- **pdfplumber** — PDF text and table extraction
- **PyInstaller** — Executable packaging
- **Inno Setup** — Windows installer creation

---

## AI Assistant

TariffMill includes an optional **AI Template Generator** that helps create PDF extraction templates for new invoice formats. This feature uses external AI APIs and has important considerations you should be aware of.

### What It Does

The AI Assistant (accessible from the **AI Templates** sub-tab within PDF Processing) provides a chat interface where you can describe an invoice format and have the AI generate Python extraction code. This is a convenience tool for creating new templates — it is **not required** for normal invoice processing or any other TariffMill feature.

### Requirements

- An API key from a supported AI provider (Anthropic Claude, OpenAI, etc.)
- Configured in Settings > AI Provider page
- AI Assistant access must be enabled for the user account (admins have it by default; other users need it granted by an admin)

### Cost Warning

> **The AI Assistant makes API calls to external AI services that charge per use.** Each interaction with the template generator sends data to the configured AI provider and incurs costs on your API account. Costs vary by provider and model but can accumulate quickly during extended template development sessions. Monitor your API provider's usage dashboard to track spending.

TariffMill does not manage, limit, or track your API spending. You are solely responsible for any charges incurred through your API key.

### Limitations and Disclaimer

> **This feature has not been extensively tested and is provided as-is.** The AI-generated templates may require manual review, correction, or debugging before they produce reliable extraction results. Generated code should always be validated against known invoice data before use in production.

Specific limitations:
- AI-generated templates may not correctly handle all edge cases in an invoice format
- Extraction accuracy depends on the quality of the AI model and the clarity of the invoice layout
- The AI may produce code with errors that require Python knowledge to fix
- Template output should be spot-checked against the original invoice before relying on it
- AI providers may change their APIs, pricing, or models at any time

### Data Sent to AI Providers

When using the AI Assistant, the following data may be sent to the configured AI provider:
- PDF text content from the invoice being used as a reference
- Your chat messages describing the invoice format
- Previously generated template code (for iterative refinement)

No data is sent to AI providers unless you explicitly use the AI Template Generator. All other TariffMill features operate entirely offline.

---

## Documentation

| Document | Description |
|----------|-------------|
| [User Guide](docs/TariffMill_User_Guide.md) | Complete guide for end users — installation, invoice processing, PDF processing, parts management, settings |
| [Admin Guide](docs/TariffMill_Admin_Guide.md) | System administration — user management, roles & permissions, authentication, database setup, backups, deployment |
| [Auto-Update Guide](docs/AUTO_UPDATE_GUIDE.md) | Auto-update system configuration and troubleshooting |
| [Architecture Flowcharts](docs/flowcharts/) | Visual diagrams of invoice processing, parts data flow, template processing, and tariff detection |

---

## Version

**Current Version**: v0.98.0

### What's New in v0.98.0

- **Open Source Release** — Free under the MIT License
- **First-Run Setup Wizard** — Create your admin account on first launch (no pre-configured users needed)
- **User Management Panel** — Add, edit, delete, suspend, and reset passwords for users directly from the Admin Panel (Ctrl+Shift+A)
- **Role-Based Access** — Admin, division admin, and user roles with appropriate permissions
- **Windows Domain Auth** — Auto-login with automatic user provisioning for allowed domains — no need to pre-register each domain user
- **Shared Templates** — Network folder support for sharing PDF extraction templates across users
- **Settings Migration** — Domain and template settings migrated to the app_config table
- **Production Hardening** — Debug print statements replaced with proper logging

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes
4. Push to your fork and open a Pull Request

For bug reports and feature requests, please use [GitHub Issues](https://github.com/ProcessLogicLabs/open-tariffmill/issues).

---

## Support

- **Issues**: [GitHub Issues](https://github.com/ProcessLogicLabs/open-tariffmill/issues)
- **Documentation**: [User Guide](docs/TariffMill_User_Guide.md) | [Admin Guide](docs/TariffMill_Admin_Guide.md)
- **Source Code**: [github.com/ProcessLogicLabs/open-tariffmill](https://github.com/ProcessLogicLabs/open-tariffmill)

## License

MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2024-2026 Process Logic Labs, LLC
