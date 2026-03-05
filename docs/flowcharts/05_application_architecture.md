# Application Architecture

This flowchart shows the overall system architecture and component relationships.

```mermaid
flowchart TD
    subgraph UI["User Interface Layer (PyQt5)"]
        A[TariffMill Main Window]
        A --> B[Invoice Processing Tab]
        A --> C[PDF Processing Tab]
        A --> D[Parts View Tab]
        A --> D2[Parts Import Tab]
        A --> E[Menu Bar]
        E --> F[Settings Dialog]
        E --> G[References Dialog]
        E --> H[Account Menu]
        E --> I2[Help Menu]
    end

    subgraph Settings["Unified Settings Dialog"]
        F --> F1[General Page]
        F --> F2[PDF Processing Page]
        F --> F3[AI Provider Page]
        F --> F4[Templates Page]
        F --> F5[Database Page]
        F --> F6[Updates Page]
        F --> F7[Authentication Page]
    end

    subgraph Business["Business Logic Layer"]
        B --> I[Invoice Processor]
        C --> J[OCR Engine]
        D --> K[Parts Manager]
        D2 --> K

        I --> L[Column Mapper]
        I --> M[Value Calculator]
        I --> N[Tariff Classifier]

        J --> O[Template Engine]
        O --> P[Template Registry]
        O --> P2[Shared Templates]
    end

    subgraph Data["Data Access Layer"]
        L --> Q[(SQLite Database)]
        M --> Q
        N --> Q
        K --> Q
        P --> R[Local Template Files]
        P2 --> R2[Network Template Files]

        Q --> S[parts_master]
        Q --> T[invoice_mappings]
        Q --> U[user_settings]
        Q --> V[hts_codes]
        Q --> V2[folder_profiles]
        Q --> V3[billing_settings]
    end

    subgraph External["External Resources"]
        W[Input Files] --> I
        I --> X[Output Files]
    end

    style A fill:#2196F3,color:#fff
    style Q fill:#4CAF50,color:#fff
    style R fill:#FF9800,color:#fff
    style F fill:#9C27B0,color:#fff
```

## Component Overview

### User Interface Layer

| Component | Description |
|-----------|-------------|
| Main Window | Primary application window with tabbed interface |
| Invoice Processing | Invoice processing and export functionality (CSV/Excel files) |
| PDF Processing | OCR processing with AI template system for PDF invoices |
| Parts View | Database management with search, query builder, and editing |
| Parts Import | Dedicated tab for bulk CSV import with column mapping |
| Menu Bar | Settings, References, Account, and Help menus |

### Unified Settings Dialog

All application settings are consolidated in **Settings > Settings**:

| Page | Description |
|------|-------------|
| General | Theme, fonts, row height, MID list |
| PDF Processing | Input/output folders, processing modes, auto-start |
| AI Provider | API keys, model selection |
| Templates | Shared templates folder, sync settings |
| Database | Database path, backup settings |
| Updates | Check for updates on startup |
| Authentication | Domain authentication settings |

### Business Logic Layer

| Component | Description |
|-----------|-------------|
| Invoice Processor | Core invoice processing engine |
| Parts Manager | CRUD operations for parts database |
| OCR Engine | Text extraction from PDF/images |
| Column Mapper | Map source columns to target fields |
| Value Calculator | Calculate quantities and distributions |
| Tariff Classifier | Determine Section 232/301 status |
| Template Engine | Match and apply OCR templates |
| Template Registry | Local and shared template discovery |

### Data Access Layer

| Component | Description |
|-----------|-------------|
| SQLite Database | Primary data storage |
| Local Template Files | Python template definitions (editable) |
| Network Template Files | Shared templates from network folder (read-only) |

## Database Schema

```mermaid
erDiagram
    parts_master {
        text part_number PK
        text hts_code
        text country_of_origin
        text mid
        real steel_ratio
        real aluminum_ratio
        real copper_ratio
        real wood_ratio
        real auto_ratio
        text country_of_melt
        text country_of_cast
        text prim_country_of_smelt
    }

    invoice_mappings {
        integer id PK
        text profile_name
        text source_column
        text target_field
        text file_pattern
    }

    folder_profiles {
        text profile_name PK
        text input_folder
        text output_folder
        text created_date
    }

    user_settings {
        text key PK
        text value
    }

    billing_settings {
        text key PK
        text value
    }

    hts_codes {
        text hts_code PK
        text description
        text qty1_unit
        text qty2_unit
    }
```

## File Structure

```
Tariffmill/
├── tariffmill.py           # Main application
├── settings_dialog.py      # Unified settings dialog
├── version.py              # Version management
├── Resources/
│   ├── tariffmill.db       # SQLite database
│   ├── icon.ico            # Application icon
│   └── References/
│       ├── hts.db          # HTS code reference database
│       └── CBP_232_tariffs.xlsx
├── templates/
│   ├── __init__.py         # Template discovery
│   ├── base_template.py    # Base template class
│   └── *.py                # Custom templates
├── invoice_processor/      # Invoice processing module
├── Input/
│   └── Processed/          # Archived input files
└── Output/
    └── Processed/          # Archived output files
```

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.12 | Core language |
| PyQt5 | Desktop GUI framework |
| Pandas | Data processing and manipulation |
| SQLite | Embedded database |
| OpenPyXL | Excel file read/write |
| pdfminer | PDF text extraction |
| Anthropic Claude | AI-powered template generation |
| PyInstaller | Executable packaging |
| Inno Setup | Windows installer |
