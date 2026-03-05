# User Workflow

This flowchart shows the end-to-end user journey for processing customs documentation.

```mermaid
flowchart TD
    subgraph Setup["Initial Setup (One-time)"]
        A[Install TariffMill] --> B[Launch Application]
        B --> C[Open Settings Dialog]
        C --> C1[General: Set Theme, MID List]
        C1 --> C2[PDF Processing: Set Folders]
        C2 --> C3[Templates: Configure Shared Folder]
        C3 --> D[Create Folder Profiles]
        D --> E[Import Parts via Parts Import Tab]
        E --> F[Create Mapping Profiles]
    end

    subgraph Daily["Daily Workflow"]
        G[Receive Invoice] --> G1[Select Folder Profile]
        G1 --> H{File Format?}
        H -->|PDF| I[Use PDF Processing Tab]
        H -->|CSV/Excel| J[Use Invoice Processing Tab]

        I --> K[Select or Auto-Match Template]
        K --> L[Extract Data]
        L --> M[Export to CSV]
        M --> J

        J --> N[Select File from Input Files List]
        N --> O[Select/Create Mapping]
        O --> P[Enter Invoice Total]
        P --> Q[Select MID from Dropdown]
        Q --> R[Click Process Invoice]
    end

    subgraph Review["Review & Edit"]
        R --> S[View Preview Table]
        S --> S1[Review Color-Coded Material Types]
        S1 --> T{Data Correct?}
        T -->|No| U[Edit Values in Table]
        U --> V[Reprocess if Needed]
        V --> S
        T -->|Yes| W[Verify Total Matches]
    end

    subgraph Export["Export & Archive"]
        W --> X[Click Export Worksheet]
        X --> Y[Choose Split Options]
        Y --> Z[Generate CBP Worksheet]
        Z --> AA[File Saved to Output Folder]
        AA --> AB[Source Moved to Processed]
        AB --> AC[Done]
    end

    subgraph Maintenance["Periodic Maintenance"]
        AD[Parts View: Search/Edit Records] --> AE[Query Builder for Complex Searches]
        AE --> AF[Parts Import: Bulk Import New Parts]
        AF --> AG[Settings > Database: Backup]
        AG --> AH[Settings > Templates: Sync Shared Templates]
    end

    style A fill:#4CAF50,color:#fff
    style AC fill:#4CAF50,color:#fff
    style T fill:#FFC107,color:#000
    style C fill:#9C27B0,color:#fff
```

## Detailed User Steps

### Initial Setup

1. **Install Application**
   - Run TariffMill_Setup.exe installer
   - Or use standalone TariffMill.exe

2. **Configure Settings** (Settings > Settings)
   - **General**: Choose theme (Light/Dark), configure MID list
   - **PDF Processing**: Set default input/output folders
   - **AI Provider**: Enter API key for AI-powered features
   - **Templates**: Configure shared templates network folder
   - **Database**: View database location, configure backups
   - **Updates**: Enable/disable automatic update checks

3. **Create Folder Profiles**
   - Invoice Processing tab → Folder Profile dropdown → Manage (gear icon)
   - Create profiles for different clients/projects
   - Each profile stores input and output folder paths

4. **Import Parts Data**
   - Parts Import tab (dedicated import interface)
   - Load CSV file → Preview data → Map columns
   - Select import mode (Insert/Update/Upsert)
   - Click Import Parts

5. **Create Mapping Profiles**
   - Process first invoice from each supplier
   - Create mapping for that invoice format
   - Save profile for future use

### Daily Invoice Processing

```mermaid
sequenceDiagram
    participant User
    participant TariffMill
    participant Database
    participant FileSystem

    User->>TariffMill: Select Folder Profile
    TariffMill->>FileSystem: Load Input Files List
    User->>TariffMill: Select Invoice File
    TariffMill->>TariffMill: Parse CSV/Excel
    User->>TariffMill: Select Mapping Profile
    TariffMill->>TariffMill: Apply Column Mapping
    User->>TariffMill: Enter Invoice Total
    User->>TariffMill: Select MID
    User->>TariffMill: Click Process Invoice
    TariffMill->>Database: Lookup Part Numbers
    Database-->>TariffMill: Return Part Data
    TariffMill->>TariffMill: Calculate Tariffs & Materials
    TariffMill->>TariffMill: Distribute Values
    TariffMill-->>User: Display Color-Coded Preview
    User->>TariffMill: Verify & Edit
    User->>TariffMill: Click Export Worksheet
    TariffMill->>FileSystem: Save Excel to Output Folder
    TariffMill->>FileSystem: Move Source to Processed
    TariffMill-->>User: Confirm Complete
```

### Quick Reference

| Task | Location | Steps |
|------|----------|-------|
| Process CSV/Excel Invoice | Invoice Processing tab | Select Folder Profile → Select File → Map → Process → Export |
| Process PDF Invoice | PDF Processing tab | Drop PDF → Select Template → Extract → Send to Invoice Processing |
| Manage Folder Profiles | Invoice Processing tab | Click gear icon next to Folder Profile dropdown |
| Add New Part | Parts View tab | Right-click → Add Row |
| Edit Part | Parts View tab | Double-click cell |
| Search Parts | Parts View tab | Use search box or Query Builder button |
| Import Parts (Bulk) | Parts Import tab | Load CSV → Map Columns → Import |
| Configure MID List | Settings > Settings > General | Edit MID List section |
| Change Theme | Settings > Settings > General | Select Light/Dark/System |
| Configure Shared Templates | Settings > Settings > Templates | Set shared folder, click Sync |
| Backup Database | Settings > Settings > Database | Click Backup Now |
| View Logs | Log View menu | View Log |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+O | Open invoice file |
| Ctrl+S | Save/Export |
| Ctrl+P | Process invoice |
| Ctrl+F | Search parts |
| Ctrl+R | Refresh/Reprocess |
| F5 | Refresh file lists |

### Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Part not found | Add via Parts View or import via Parts Import tab |
| Values don't match | Edit directly in preview table |
| Wrong HTS code | Update in Parts View tab |
| Missing MID | Add to MID list in Settings > General |
| Export fails | Check output folder permissions |
| Shared templates not showing | Check Settings > Templates folder path |
| Folder profile not applying | Click Sync or reselect the profile |
