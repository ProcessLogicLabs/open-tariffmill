# Parts Master Data Flow

This flowchart shows how parts data is managed, imported, and used throughout the application.

```mermaid
flowchart TD
    subgraph DataSources["Data Sources"]
        A[CSV Import File]
        B[Manual Entry in Parts View]
        C[Invoice Processing]
    end

    subgraph Import["Parts Import Tab"]
        A --> D[Load CSV File]
        D --> E[Preview Data in Table]
        E --> F[Map CSV Columns to DB Fields]
        F --> G[Select Import Mode]
        G --> G1{Mode?}
        G1 -->|Insert Only| H1[Skip Existing Parts]
        G1 -->|Update Only| H2[Update Existing Parts]
        G1 -->|Upsert| H3[Insert or Update]
        H1 --> I[Import to Database]
        H2 --> I
        H3 --> I
    end

    subgraph Database["SQLite Database"]
        I --> J[(parts_master)]
        B --> J
        J --> K[Part Number]
        J --> L[HTS Code]
        J --> M[Country of Origin]
        J --> N[MID]
        J --> O[Material Ratios]
        J --> P[Melt/Cast/Smelt Countries]
    end

    subgraph Usage["Data Usage"]
        C --> Q[Lookup Part Number]
        Q --> J
        J --> R[Return Part Data]
        R --> S[Apply to Invoice Line]
    end

    subgraph Query["Query & Search in Parts View"]
        T[Quick Search Box] --> J
        U[Query Builder Dialog] --> V[Build SQL Query]
        V --> J
        J --> W[Display Results in Table]
        W --> W2[Export to CSV]
    end

    subgraph Maintenance["Data Maintenance"]
        X[Double-click to Edit Cell] --> J
        Y[Right-click Delete Row] --> J
        Z[Bulk Column Update] --> J
    end

    style J fill:#2196F3,color:#fff
    style G1 fill:#FFC107,color:#000
    style I fill:#4CAF50,color:#fff
    style D fill:#9C27B0,color:#fff
```

## Data Structure

### Parts Master Table Fields
| Field | Description | Used For |
|-------|-------------|----------|
| part_number | Unique part identifier | Primary lookup key |
| hts_code | Harmonized Tariff Schedule code | Duty calculation |
| country_of_origin | Country where product originated | CBP declaration |
| mid | Manufacturer ID | Customs identification |
| steel_ratio | Percentage of steel content | Section 232 |
| aluminum_ratio | Percentage of aluminum content | Section 232 |
| copper_ratio | Percentage of copper content | Section 232 |
| wood_ratio | Percentage of wood content | Section 232 |
| auto_ratio | Percentage classified as automotive | Section 232 |
| country_of_melt | Steel melt country | Section 232 declaration |
| country_of_cast | Steel cast country | Section 232 declaration |
| prim_country_of_smelt | Primary smelt country | Section 232 declaration |

## Parts Import Tab

The Parts Import tab provides a dedicated interface for bulk importing parts data:

1. **Load CSV File** - Click "Load CSV" to select a file
2. **Preview Data** - View the CSV data in a table before importing
3. **Map Columns** - Use the Column Mapping section to match CSV columns to database fields
4. **Select Import Mode**:
   - **Insert Only** - Only add new parts, skip existing part numbers
   - **Update Only** - Only update existing parts, skip new part numbers
   - **Upsert** - Insert new parts and update existing parts
5. **Import** - Click "Import Parts" to execute the import

## Parts View Tab

The Parts View tab provides full CRUD operations:

### Quick Search
- Type in the search box to filter by any field
- Results update as you type

### Query Builder
- Click "Query Builder" button for advanced searches
- Build complex queries with multiple conditions
- Combine conditions with AND/OR logic
- Export query results to CSV

### Editing Data
- **Edit**: Double-click any cell to edit in place
- **Add Row**: Right-click > Add Row
- **Delete Row**: Right-click > Delete Row
- **Bulk Update**: Select column, enter value, apply to all visible rows
