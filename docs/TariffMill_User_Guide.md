# TariffMill User Guide

**Professional Customs Documentation Processing System**

Version 0.98.0 | Open Source Edition | March 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [System Requirements](#2-system-requirements)
3. [Installation](#3-installation)
4. [First-Time Setup](#4-first-time-setup)
5. [Logging In](#5-logging-in)
6. [Application Layout](#6-application-layout)
7. [Invoice Processing](#7-invoice-processing)
8. [PDF Processing (OCRMill)](#8-pdf-processing-ocrmill)
9. [Parts Database Management](#9-parts-database-management)
10. [Reference Data](#10-reference-data)
11. [Master Data & Profiles](#11-master-data--profiles)
12. [Settings & Preferences](#12-settings--preferences)
13. [e2Open Integration](#13-e2open-integration)
14. [Auto-Updates](#14-auto-updates)
15. [Keyboard Shortcuts](#15-keyboard-shortcuts)
16. [Troubleshooting](#16-troubleshooting)
17. [Appendix](#17-appendix)

---

## 1. Introduction

TariffMill is a free, open-source desktop application designed for import/export businesses, customs brokers, and trade compliance professionals. It automates commercial invoice processing, manages parts databases with HTS classifications, and ensures compliance with U.S. Section 232 and Section 301 tariff requirements.

### What TariffMill Does

- **Transforms commercial invoices** into customs-ready upload worksheets for e2Open and other customs management systems
- **Extracts invoice data from PDFs** using AI-powered templates — no manual data entry required
- **Manages a parts master database** with HTS codes, material compositions, country of origin, and melt/cast/smelt declarations
- **Automates Section 232 derivative calculations** — splits line items by steel, aluminum, copper, wood, and automotive content with prorated values
- **Tracks Section 301 exclusions** with expiration dates
- **Generates CBP-compliant quantity units** from the built-in HTS database

### Who Should Use This Guide

This guide is for **end users** who process invoices, manage parts data, and use the PDF extraction features. For system administration tasks (user management, domain configuration, backups), see the [TariffMill Admin Guide](TariffMill_Admin_Guide.md).

---

## 2. System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Operating System | Windows 10 | Windows 11 |
| RAM | 4 GB | 8 GB |
| Disk Space | 200 MB | 500 MB |
| Display | 1280 x 720 | 1920 x 1080 |
| Network | Not required | For shared database & templates |

### Supported Platforms

| Platform | Installation Method |
|----------|-------------------|
| **Windows** | Installer (.exe) or portable executable |
| **Linux** | pip install from GitHub |
| **macOS** | pip install from GitHub |

---

## 3. Installation

### Windows Installer (Recommended)

1. Download `TariffMill_Setup_x.xx.x.exe` from the [Releases](https://github.com/ProcessLogicLabs/open-tariffmill/releases) page
2. Run the installer and follow the prompts
3. Launch TariffMill from the Start Menu or Desktop shortcut

### Windows Portable

1. Download `TariffMill.exe` from the Releases page
2. Place it in your preferred folder
3. Double-click to run — no installation required

> **Note:** The portable version stores its database and settings locally alongside the executable. It is ideal for USB drives or environments where you cannot install software.

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
source venv/bin/activate        # Linux/macOS
.\venv\Scripts\activate         # Windows
pip install -r requirements.txt
python Tariffmill/tariffmill.py
```

### Windows SmartScreen Warning

On first run, Windows may display **"Windows protected your PC"** because the application is new. To proceed:

1. Click **"More info"**
2. Click **"Run anyway"**

---

## 4. First-Time Setup

When TariffMill launches for the first time and no user accounts exist, it displays a **First-Run Setup Wizard** to create your admin account.

### Step 1: Create Your Admin Account

| Field | Description | Rules |
|-------|-------------|-------|
| **Name** | Your display name | Required |
| **Email** | Your login email | Required, must contain `@` |
| **Password** | Account password | Required, minimum 6 characters |
| **Confirm Password** | Re-enter password | Must match password |

Fill in the form and click **Create Account**. Your credentials are saved to `auth_users.json` in the application directory.

### Step 2: Log In

After the admin account is created, the Login dialog appears. Enter the email and password you just created.

### Step 3: Configure Your Folders

Once logged in, go to **Settings** > **Settings...** and set your **Input Folder** and **Output Folder** paths. Alternatively, create a **Folder Profile** from the Invoice Processing tab.

### Step 4: Import Reference Data

Go to the **References** menu:

1. **HTS Database...** — Import your HTS tariff data (JSON or CSV from USITC)
2. **Section 232 Tariffs...** — Import Section 232 tariff classifications
3. **Section 232 Actions...** — Import Chapter 99 action codes

### Step 5: Set Up Your Parts Database

Go to **Master Data** > **Master Data...** > **Parts Import** tab to bulk-import your parts with HTS codes and material compositions.

---

## 5. Logging In

### Email/Password Login

1. Enter your **Email** and **Password**
2. Click **Sign In**

The email field remembers your last login for convenience.

### Windows Domain Auto-Login

If your administrator has configured Windows domain authentication, TariffMill will automatically log you in using your Windows credentials. No login dialog is shown.

### Signing Out

Go to **Session** > **Sign Out** to log out and return to the login screen.

---

## 6. Application Layout

### Menu Bar

| Menu | Purpose |
|------|---------|
| **Session** | Current user info, sign out, division user management |
| **Settings** | Application preferences and configuration |
| **Master Data** | Invoice mapping profiles, output mapping, parts import, MID management |
| **References** | HTS database, Section 232 tariffs, Section 232 actions |
| **Help** | Check for updates, view log, statistics, about |

### Main Tabs

| Tab | Purpose |
|-----|---------|
| **Invoice Processing** | Process CSV/Excel invoices into customs-ready worksheets |
| **PDF Processing** | Extract data from PDF invoices using AI templates |
| **Parts View** | Search, edit, and manage the parts master database |

---

## 7. Invoice Processing

The Invoice Processing tab is the primary workflow for converting commercial invoices into customs-ready upload worksheets.

### Workflow Overview

```
Select Invoice -> Enter Values -> Process -> Review -> Export
```

### Left Panel

#### Shipment File Section

1. **Folder Profile** dropdown — Switch between saved input/output folder sets
2. **Map Profile** dropdown — Choose an invoice column mapping profile
3. **Input Files** list — Shows CSV and Excel files in the input folder
4. **Refresh** / **Delete** / **Sort** buttons

#### Invoice Values Section

| Field | Description | Required |
|-------|-------------|----------|
| **CI Value (USD)** | Total commercial invoice value in US dollars | Yes |
| **Net Weight (kg)** | Shipment total net weight in kilograms | No |
| **MID** | Manufacturer ID — select from dropdown (type to search) | Yes |
| **Division** | Business division (if configured) | Conditional |
| **File Number** | Reference number for the entry | Yes |

**Invoice Check** indicator:
- **Green checkmark** — Values match the calculated totals
- **Red X** — Discrepancy detected; click **Edit Values** to correct

#### Action Buttons

| Button | Action |
|--------|--------|
| **Process Invoice** | Process the selected invoice against the parts database |
| **Reprocess** | Re-process to pick up database changes since last run |
| **Add Missing** | Open dialog to add unmatched parts to the database |
| **Clear All** | Clear the current session and start fresh |

#### Exported Files Section

Shows previously exported CSV files. Double-click to open in Excel.

### Right Panel — Result Preview

After processing, the result preview table displays all line items with their tariff data.

#### Color-Coded Rows

| Color | Meaning |
|-------|---------|
| **Gray** | Steel content (Declaration Code 08) |
| **Blue** | Aluminum content (Declaration Code 07) |
| **Orange** | Copper content |
| **Brown** | Wood content |
| **Dark Green** | Automotive content |
| **White** | Non-232 items |
| **Highlighted** | Section 301 exclusion items |

#### Working with the Preview

- **Double-click** a cell to edit its value
- **Right-click** a column header for options: auto-fit width, reset widths
- Column widths and visibility are saved per user

### Exporting

Click **Export Worksheet** after reviewing. The file is saved as `InvoiceName_YYYYMMDD_HHMMSS.xlsx`.

### Section 232 Derivative Processing

TariffMill automatically creates derivative line items for materials subject to Section 232 tariffs:

1. Each line item with material content is split into derivative lines
2. Values are prorated based on material percentages from the parts database
3. Declaration codes are assigned: **08** (Steel), **07** (Aluminum)
4. Country of melt/pour/cast/smelt codes are populated from the parts database

**Example:** A $1,000 part with 30% steel and 10% aluminum becomes:

| Line | Value | Declaration |
|------|-------|------------|
| Original | $600 | (remaining value) |
| Steel derivative | $300 | Code 08 |
| Aluminum derivative | $100 | Code 07 |

---

## 8. PDF Processing (OCRMill)

The PDF Processing tab extracts invoice data from PDF documents using AI-powered templates.

### Invoice Processing Sub-Tab

#### Input Files (PDFs)

Lists PDF files in your configured input folder. Click **Refresh** to rescan. Double-click to open in your default PDF viewer.

#### Output Files (CSVs)

Lists extracted CSV results. Click to preview. Use **Refresh** to rescan and **Delete** to remove a file.

#### Processing Actions

| Button | Action |
|--------|--------|
| **Start Monitoring** | Toggle folder monitoring — auto-process new PDFs |
| **Process PDF File...** | Process a single selected PDF |
| **Process Folder Now** | Batch-process all PDFs in the input folder |
| **Send to Tariffmill** | Move extracted CSV to the Invoice Processing tab |

#### Drag & Drop

Drag PDF files directly onto the **Drop Zone** at the top of the right panel.

#### Multi-invoice Output Mode

- **Split** — One CSV per invoice
- **Combine** — All invoices merged into a single CSV

### AI Templates Sub-Tab

> **Note:** This tab is only visible if your account has AI Assistant access (granted by an admin).

The AI Templates tab provides an integrated template editor with a chat interface powered by an external AI service. Use it to create or modify PDF extraction templates for specific invoice formats.

> **Cost Warning:** The AI Template Generator makes API calls to external AI services (Anthropic Claude, OpenAI, etc.) that **charge per use**. Each interaction incurs costs on your API account. Monitor your provider's usage dashboard to track spending. TariffMill does not manage or limit your API usage.
>
> **Disclaimer:** This feature has not been extensively tested and is provided as-is. AI-generated templates may contain errors and should always be validated against known invoice data before use in production. Generated code may require Python knowledge to review and correct.

### Template System Overview

Templates define how TariffMill extracts data from specific invoice formats. Each template calculates a **confidence score** (0-1.0) and the highest-scoring template is used.

**Template sources:**
- **Bundled templates** — Included with the application
- **Shared templates** — Loaded from a network folder (configured in Settings)
- **Local templates** — Custom templates you create

**Extracted fields:** Part Number, Description, Quantity, Unit Price, Extended Value, Country of Origin, HTS Code (if on invoice)

### Sending to Invoice Processing

1. Select output file in the **Output Files** list
2. Click **Send to Tariffmill**
3. Data transfers to the Invoice Processing tab for tariff application

---

## 9. Parts Database Management

The **Parts View** tab provides full access to your parts master database.

### Parts Table Columns

| Column | Description | Editable |
|--------|-------------|----------|
| Part Number | Unique identifier (primary key) | Yes |
| Description | Part description | Yes |
| HTS Code | 10-digit Harmonized Tariff Schedule code | Yes |
| Country of Origin | Manufacturing country | Yes |
| MID | Manufacturer ID | Yes |
| Client Code | Customer/client identifier | Yes |
| Steel / Aluminum / Copper / Wood / Auto % | Material percentages (0-100) | Yes |
| Qty Unit | CBP quantity unit of measure | Yes |
| HTS Verified | Verification status | Yes |
| Sec 301 Exclusion | Section 301 exclusion tariff code | Yes |
| Created Date | When the part was first added | Read-only |
| Updated Date | When the part was last modified | Read-only |

### Action Buttons

| Button | Action |
|--------|--------|
| **Add Row** | Insert a new blank part entry |
| **Delete Selected** | Remove selected parts from the database |
| **Save Changes** | Persist all edits to the database |
| **Refresh** | Reload parts from the database |
| **Export Missing HTS** | Export parts missing CBP quantity units |
| **Verify HTS** | Validate all HTS codes against the reference database |
| **Export by Client** | Filter and export parts for a specific client |

### Searching Parts

#### Quick Search Presets

| Preset | What It Shows |
|--------|--------------|
| **Show All Parts** | Entire parts database |
| **Missing HTS Codes** | Parts without an HTS code |
| **Invalid HTS Codes** | Parts with HTS codes not in the reference database |
| **Steel Parts** | Parts with steel percentage > 0% |
| **Aluminum Parts** | Parts with aluminum percentage > 0% |

#### Search by Field

Select a field (Part Number, Description, HTS Code, Country, MID, Client, etc.), a match type (Contains, Equals, Starts with, etc.), and enter your search term.

#### Custom SQL

Check **Show Advanced SQL** to enter custom queries like:

```sql
SELECT * FROM parts_master WHERE steel_pct > 50 AND country_origin = 'CN'
```

#### Table Filter

The filter bar above the table lets you type to instantly filter visible rows. Use **Export Visible Rows** to export the current filtered view.

### Importing Parts

1. Go to **Master Data** > **Master Data...** > **Parts Import** tab
2. Click **Load CSV/Excel File**
3. Map source columns to target fields (Part Number and HTS Code are required)
4. Preview the import, then click **Import Now**

---

## 10. Reference Data

Access reference databases via the **References** menu.

### HTS Database (References > HTS Database...)

Import HTS data via JSON (recommended) or CSV from USITC. Search by HTS code to view full tariff descriptions, duty rates, and units of quantity.

### Section 232 Tariffs (References > Section 232 Tariffs...)

Manage Section 232 tariff classifications. Filter by material type, view Chapter 99 codes and duty rates. Import from CSV/Excel.

### Section 232 Actions (References > Section 232 Actions...)

Manage Chapter 99 tariff action codes with effective/expiration dates, rates, and declaration requirements.

---

## 11. Master Data & Profiles

Access via **Master Data** > **Master Data...**

### Invoice Mapping Profiles

Save column mapping configurations for different invoice formats. Select from the **Map Profile** dropdown on the Invoice Processing tab.

### Output Mapping

Control which columns appear in exports, their order, and material colors. Save as reusable profiles.

### Parts Import

Bulk-import parts from Excel or CSV with column mapping and duplicate handling.

### MID Management

Manage Manufacturer IDs: MID code, manufacturer name, customer ID, and related parties (Y/N).

### Folder Profiles

Create named input/output folder pairs for quick switching. Folder profiles are per-user. The last-used profile is restored on startup.

---

## 12. Settings & Preferences

Access via **Settings** > **Settings...**

### General Settings

Theme (7 options), font size (8-16pt), preview row height (22-40px), window geometry persistence.

### PDF Processing Settings

Input/output folder paths, poll interval, auto-start monitoring, multi-invoice consolidation.

### AI Provider Settings

AI service provider, API key, model selection, temperature, token limit.

> **Note:** Configuring an AI provider API key enables the AI Template Generator, which incurs costs per API call. See the [AI Assistant](#ai-templates-sub-tab) section for important cost and limitation details.

### Templates Settings

Shared templates folder (network path), local templates folder.

### Database Settings

Database path, backup folder, auto-backup toggle, backup frequency, retention count, designated backup machine.

### Updates Settings

Check for updates on startup, silent installation mode.

---

## 13. e2Open Integration

TariffMill exports are pre-mapped for direct upload to e2Open Customs Management.

### Column Mapping Reference

| TariffMill Column | e2Open Field |
|-------------------|--------------|
| Part Number | Part Number |
| Value | Value |
| MID | Manufacturer |
| HTS | Tariff No |
| Qty 1 Unit | Qty 1 Class |
| Qty 2 Unit | Qty 2 Class |
| Declaration Code | Declaration Type Cd |
| Country Melt Pour | Country Melt Pour Cd |
| Country Cast | Country Cast |
| Primary Country Smelt | Primary Country Smelt |

### Benefits

- No manual line splitting — derivative lines pre-created with prorated values
- No declarations dialog — melt/smelt/cast codes pre-populated
- CBP quantities from HTS database
- Direct upload — no reformatting required

---

## 14. Auto-Updates

TariffMill checks for new versions on GitHub and can install updates automatically.

1. On startup (if enabled), checks the GitHub Releases API
2. If a newer version is found, shows a notification with release notes
3. Click **Download & Install** for automatic installation, or **View on GitHub** for manual download

Configure in **Settings** > **Updates** page. Manual check: **Help** > **Check for Updates...**

---

## 15. Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+A` | Open Admin Panel (admin users only) |
| `F5` | Refresh current tab |
| `Enter` | Process/search (context-dependent) |
| `Double-click` | Edit a table cell |

---

## 16. Troubleshooting

### Common Issues

| Problem | Cause | Fix |
|---------|-------|-----|
| "File Number Required" | Empty or invalid file number | Enter a valid file number matching the division's format |
| Values don't match | Calculated total differs from CI Value | Click **Edit Values** to review and correct line items |
| Parts not found | Part numbers don't match database | Click **Add Missing** or import via Parts Import |
| PDF extraction fails | No matching template or image-only PDF | Create a template or ensure PDF has a text layer |
| App doesn't start | Missing dependencies | Reinstall from the latest release |

### Viewing Logs

Go to **Help** > **View Log** to see detailed application logs.

### Getting Help

- **GitHub Issues:** [github.com/ProcessLogicLabs/open-tariffmill/issues](https://github.com/ProcessLogicLabs/open-tariffmill/issues)
- **Source Code:** [github.com/ProcessLogicLabs/open-tariffmill](https://github.com/ProcessLogicLabs/open-tariffmill)

---

## 17. Appendix

### Supported File Formats

| Direction | Formats |
|-----------|---------|
| **Input** | CSV (.csv), Excel (.xlsx, .xls), PDF (.pdf) |
| **Output** | Excel Workbook (.xlsx) |

### Material Declaration Codes

| Code | Material |
|------|----------|
| 07 | Aluminum and aluminum derivatives |
| 08 | Steel and steel derivatives |

### Data Privacy

- Commercial invoice data is **not stored** permanently — it passes through for transformation only
- No telemetry or analytics are collected
- No data is sent to external servers (except optional AI API calls for template generation)
- All data remains on your machine or your configured network database

### Settings Storage

| Location | What's Stored | Scope |
|----------|--------------|-------|
| **SQLite database** (app_config table) | Shared settings, allowed domains, template paths | All users |
| **Windows Registry** (HKCU\Software\TariffMill) | Theme, font size, window geometry, column widths | Per user |
| **auth_users.json** | User accounts, passwords (hashed), roles | All users |
| **config.ini** | Database path, backup settings | Per installation |

---

*TariffMill — Professional Customs Documentation Processing*

*Open Source Edition — MIT License*

*Copyright (c) 2024-2026 Process Logic Labs, LLC*
