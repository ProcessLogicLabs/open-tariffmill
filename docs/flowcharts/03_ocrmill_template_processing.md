# PDF Processing Template System

This flowchart shows how the PDF Processing tab processes invoices using the template system.

```mermaid
flowchart TD
    subgraph Input["1. Document Input"]
        A[PDF/Image Invoice] --> B[OCR Engine]
        B --> C[Extract Raw Text]
    end

    subgraph TemplateDiscovery["2. Template Discovery"]
        D1[Local Templates Directory] --> E[Scan for .py Files]
        D2[Shared Templates Directory] --> E
        E --> F[Load Template Classes]
        F --> G[Build Template Registry]
        G --> G2[Mark Shared Templates with Network Icon]
    end

    subgraph Matching["3. Template Matching"]
        C --> H[For Each Template]
        G2 --> H
        H --> I[Call can_process]
        I --> J{Match?}
        J -->|Yes| K[Calculate Confidence Score]
        J -->|No| L[Try Next Template]
        L --> H
        K --> M[Add to Candidates]
        M --> N{More Templates?}
        N -->|Yes| H
        N -->|No| O[Select Best Match]
    end

    subgraph Extraction["4. Data Extraction"]
        O --> P[Selected Template]
        P --> Q[extract_invoice_number]
        P --> R[extract_project_number]
        P --> S[extract_line_items]
        Q --> T[Invoice Data]
        R --> T
        S --> T
    end

    subgraph Output["5. Output"]
        T --> U[Structured Data]
        U --> V[Display in UI]
        U --> W[Export to CSV]
        W --> X[Send to Invoice Processing]
    end

    subgraph TemplateManagement["Template Management"]
        Y1[Settings > Templates] --> Y2[Configure Shared Folder]
        Y2 --> Y3[Sync Templates Button]
        Y3 --> Y4{Sync Direction}
        Y4 -->|Upload| Y5[Local → Shared]
        Y4 -->|Download| Y6[Shared → Local]
        Y5 --> Y7[Two-way Sync Complete]
        Y6 --> Y7
    end

    style A fill:#9C27B0,color:#fff
    style O fill:#4CAF50,color:#fff
    style U fill:#2196F3,color:#fff
    style Y1 fill:#FF9800,color:#fff
```

## Template System Architecture

### Template Locations

**Local Templates** (editable):
```
Tariffmill/templates/
├── __init__.py          # Dynamic discovery logic
├── base_template.py     # Base class for all templates
├── sample_template.py   # Example template (excluded)
└── *.py                 # Custom templates
```

**Shared Templates** (read-only, network):
```
\\Network\Share\Templates\    # Configured in Settings > Templates
└── *.py                      # Shared templates (marked with network icon)
```

### Template Interface

Each template must implement:

```python
class MyTemplate(BaseTemplate):
    name = "Template Name"
    description = "Template description"
    client = "Client/Vendor name"
    version = "1.0.0"
    enabled = True

    def can_process(self, text: str) -> bool:
        """Check if this template can process the text"""
        pass

    def get_confidence_score(self, text: str) -> float:
        """Return 0.0-1.0 confidence score"""
        pass

    def extract_invoice_number(self, text: str) -> str:
        """Extract invoice number from text"""
        pass

    def extract_line_items(self, text: str) -> List[Dict]:
        """Extract line items from text"""
        pass
```

## Matching Algorithm

1. **Load All Templates** - Scan local and shared directories for Python files
2. **Filter Enabled** - Only consider templates with `enabled = True`
3. **Test Each Template** - Call `can_process()` on extracted text
4. **Score Matches** - Calculate confidence scores for matching templates
5. **Select Best** - Choose template with highest confidence score

## Template Sharing

### Shared Templates Configuration

Configure shared templates via **Settings > Templates**:

1. **Shared Folder** - Set a network path for shared templates
2. **Save & Refresh** - Save the path and reload templates
3. **Sync Templates** - Two-way sync between local and shared folders

### Sync Behavior

The **Sync Templates** button performs bidirectional synchronization:

- **Upload**: Copies newer local templates to the shared folder
- **Download**: Copies newer shared templates to local folder
- **New templates**: Copied in both directions
- Uses file modification timestamps to determine which version is newer

### Working with Shared Templates

- Shared templates appear with a **network indicator** in the template dropdown
- Shared templates are **read-only** - you cannot edit them directly
- To modify a shared template: Right-click > **Copy to Local**
- Edit the local copy, then sync back to shared

## Hot Reload

Templates support hot reload:
- Click **Refresh** button to rescan directories
- New templates are automatically discovered
- Modified templates are reloaded
- Deleted templates are removed from registry
