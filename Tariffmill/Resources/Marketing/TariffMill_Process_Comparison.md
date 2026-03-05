# TariffMill: Customs Data Preparation Automation

## The Missing Link in Your Customs Workflow

TariffMill bridges the gap between supplier invoices and customs entry software, automating the most time-consuming step in the import process: **data preparation**.

---

## Three Ways to Process Customs Data

### 1. FULLY MANUAL PROCESS

Without any automation, customs specialists must:

| Step | Manual Task | Time |
|------|-------------|------|
| 1 | Open PDF invoice, manually read each line item | 2-5 min |
| 2 | Type part numbers into spreadsheet one by one | 5-10 min |
| 3 | Look up each part in separate database or ERP system | 10-30 min |
| 4 | Search HTS schedule for correct tariff codes | 15-45 min |
| 5 | Determine material type (steel, aluminum, etc.) from HTS | 5-10 min |
| 6 | Calculate material percentages, split rows for mixed materials | 10-20 min |
| 7 | Distribute weights proportionally across split rows | 5-10 min |
| 8 | Look up Manufacturer ID (MID) for each supplier | 5-10 min |
| 9 | Assign Section 232 declaration codes (01-11) | 5-10 min |
| 10 | Verify invoice total matches sum of line items | 2-5 min |
| 11 | Format Excel worksheet with proper layout | 10-15 min |
| 12 | Organize and archive files | 1-2 min |

**Total Time: 75-175 minutes per invoice**

---

### 2. CUSTOMS ENTRY SOFTWARE (E2Open, Descartes, etc.)

Customs management platforms like E2Open provide powerful entry filing capabilities:

| What They Do Well | What They Don't Do |
|-------------------|-------------------|
| Direct filing to CBP in 28+ countries | Extract data from supplier PDF invoices |
| Regulatory compliance checking | Look up your parts database for HTS codes |
| Declaration format standardization | Calculate Section 232 material splits |
| Global trade content (230+ countries) | Distribute weights by material percentage |
| Entry tracking and audit trails | Auto-assign declaration codes from HTS |
| Duty calculation and payment | Match parts to your internal part numbers |

**The Gap:** Customs entry software expects **clean, structured data** as input. Someone still needs to:
- Extract line items from supplier invoices (PDF/paper)
- Look up HTS codes for each part number
- Determine material composition percentages
- Split rows by Section 232 material type
- Calculate proportional weights
- Assign declaration codes

**This data preparation takes 60-150 minutes per invoice** before you can even begin entry in E2Open.

---

### 3. TARIFFMILL + CUSTOMS ENTRY SOFTWARE

TariffMill automates the **data preparation layer** that customs entry software assumes is already done:

| TariffMill Automation | Benefit |
|-----------------------|---------|
| **PDF Invoice OCR** | Extracts line items automatically from 22+ supplier templates |
| **Parts Database Lookup** | Instant HTS code, MID, and material data for known parts |
| **Section 232 Classification** | Auto-assigns material type (Steel, Aluminum, Copper, Wood, Auto) |
| **Material Row Expansion** | Splits mixed-material parts into separate declaration rows |
| **Proportional Weight Distribution** | Calculates weight allocation by value ratio |
| **Declaration Code Assignment** | Maps HTS codes to codes 01-11 automatically |
| **Invoice Validation** | Real-time total verification before export |
| **Formatted Export** | Color-coded Excel ready for entry software import |

**Total Time: 2-5 minutes per invoice**

---

## Side-by-Side Comparison

| Metric | Manual | E2Open Only | TariffMill + E2Open |
|--------|--------|-------------|---------------------|
| **Data prep time** | 75-175 min | 60-150 min | 2-5 min |
| **Entry filing time** | N/A | 10-15 min | 10-15 min |
| **Total time per invoice** | 75-175 min | 70-165 min | 12-20 min |
| **HTS lookup** | Manual search | Manual input | Auto from database |
| **Section 232 splits** | Calculator | Manual entry | Automatic |
| **Weight distribution** | Calculator | Manual entry | Automatic |
| **Declaration codes** | Reference lookup | Manual selection | Auto from HTS |
| **Error rate** | High | Medium | Low |
| **Batch processing** | No | Limited | Yes (parallel) |
| **Folder monitoring** | No | No | Yes (auto-detect) |

---

## The TariffMill Advantage

### Time Savings
- **95% reduction** in data preparation time
- Process **10-20 invoices** in the time it takes to manually prepare one
- **Batch processing** handles entire folders automatically

### Accuracy
- **Database-driven** HTS codes eliminate lookup errors
- **Automatic calculations** prevent math mistakes
- **Invoice validation** catches discrepancies before filing
- **Consistent formatting** reduces entry rejections

### Section 232 Compliance
- **Automatic material classification** from HTS codes
- **Correct declaration codes** (01-11) assigned automatically
- **Smelt & cast flags** set per CBP requirements
- **Material percentage splits** calculated precisely

### Seamless Integration
- **Export formats** compatible with major customs entry systems
- **Color-coded worksheets** for easy visual verification
- **Structured data** ready for import or copy/paste

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         IMPORT CUSTOMS WORKFLOW                          │
└─────────────────────────────────────────────────────────────────────────┘

  SUPPLIER                    TARIFFMILL                   CUSTOMS ENTRY
  INVOICES                   (Data Prep)                    SOFTWARE
                                                          (E2Open, etc.)
     │                            │                             │
     │  PDF Invoice               │                             │
     │  ──────────────────────►   │                             │
     │                            │                             │
     │                     ┌──────┴──────┐                      │
     │                     │   OCR &     │                      │
     │                     │  Template   │                      │
     │                     │  Extraction │                      │
     │                     └──────┬──────┘                      │
     │                            │                             │
     │                     ┌──────┴──────┐                      │
     │                     │   Parts     │                      │
     │                     │  Database   │                      │
     │                     │   Lookup    │                      │
     │                     └──────┬──────┘                      │
     │                            │                             │
     │                     ┌──────┴──────┐                      │
     │                     │  Section    │                      │
     │                     │    232      │                      │
     │                     │ Processing  │                      │
     │                     └──────┬──────┘                      │
     │                            │                             │
     │                     ┌──────┴──────┐                      │
     │                     │   Export    │                      │
     │                     │ Formatted   │                      │
     │                     │   Excel     │                      │
     │                     └──────┬──────┘                      │
     │                            │                             │
     │                            │  Clean, Structured Data     │
     │                            │  ─────────────────────────► │
     │                            │                             │
     │                            │                      ┌──────┴──────┐
     │                            │                      │   Entry     │
     │                            │                      │   Filing    │
     │                            │                      │   to CBP    │
     │                            │                      └──────┬──────┘
     │                            │                             │
     │                            │                             ▼
     │                            │                        FILED ENTRY
```

---

## ROI Calculator

| Scenario | Manual | With TariffMill | Savings |
|----------|--------|-----------------|---------|
| **10 invoices/day** | 12.5-29 hrs | 0.3-0.8 hrs | 12-28 hrs/day |
| **50 invoices/week** | 62-145 hrs | 1.7-4.2 hrs | 60-141 hrs/week |
| **200 invoices/month** | 250-583 hrs | 6.7-16.7 hrs | 243-567 hrs/month |

At $50/hour labor cost:
- **Monthly savings: $12,150 - $28,350**
- **Annual savings: $145,800 - $340,200**

---

## Key Differentiators

| Feature | TariffMill | Generic OCR | Customs Software |
|---------|------------|-------------|------------------|
| Supplier-specific templates | 22+ built-in | Generic only | None |
| Section 232 automation | Full support | None | Manual entry |
| Parts database integration | Native | None | Import only |
| Material percentage splits | Automatic | None | Manual |
| Weight distribution | Automatic | None | Manual |
| Declaration code mapping | HTS-based | None | Manual selection |
| Folder monitoring | Real-time | None | None |
| Batch PDF processing | Parallel | Sequential | None |

---

## Summary

**TariffMill is not a replacement for customs entry software—it's the essential preparation layer that makes entry software actually efficient.**

Without TariffMill:
- Data preparation consumes 80%+ of total processing time
- Manual lookups and calculations introduce errors
- Section 232 compliance requires constant reference checking

With TariffMill:
- Data preparation drops to minutes, not hours
- Database-driven accuracy eliminates lookup errors
- Section 232 automation ensures compliance

**TariffMill + Your Customs Entry Software = Complete Automation**

---

*TariffMill - Automating the work before the work*

© 2024 Process Logic Labs. All rights reserved.
