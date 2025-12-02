# Quick Reference Guide - ClinicalTrials.gov MCP Server

Common query patterns and use cases for the ClinicalTrials.gov MCP Server.

## Basic Searches

### Search by Condition

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Depression"
  page_size: 20
```

**Common conditions:**
- Depression
- Type 2 Diabetes
- Breast Cancer
- Alzheimer's Disease
- COVID-19
- Hypertension
- Asthma
- PTSD
- Schizophrenia
- Multiple Sclerosis

### Search by Intervention/Drug

```
Tool: search_clinical_trials
Parameters:
  query_intr: "Pembrolizumab"
  page_size: 20
```

**Common interventions:**
- Pembrolizumab
- Nivolumab
- Cognitive Behavioral Therapy
- Ketamine
- Insulin
- Metformin
- SSRI
- Radiotherapy

### Combined Condition + Intervention

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Melanoma"
  query_intr: "Pembrolizumab"
  page_size: 20
```

## Filtering by Status

### Find Recruiting Trials

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Anxiety"
  filter_overallStatus: ["RECRUITING"]
```

### Valid Status Values:
- `RECRUITING` - Currently enrolling participants
- `NOT_YET_RECRUITING` - Not yet open for enrollment
- `ACTIVE_NOT_RECRUITING` - Ongoing but not enrolling
- `COMPLETED` - Study has concluded
- `SUSPENDED` - Temporarily paused
- `TERMINATED` - Stopped early
- `WITHDRAWN` - Withdrawn before enrollment
- `ENROLLING_BY_INVITATION` - Only enrolling invited participants

### Multiple Statuses

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Depression"
  filter_overallStatus: ["RECRUITING", "NOT_YET_RECRUITING"]
```

## Location-Based Searches

### Search by City/State

```
Tool: search_clinical_trials
Parameters:
  query_locn: "Boston"
  query_cond: "Cancer"
```

### Search by Institution

```
Tool: search_clinical_trials
Parameters:
  query_locn: "Mayo Clinic"
```

### Geographic Radius Search

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Diabetes"
  filter_geo: "distance(40.7128,-74.0060,50mi)"
```

Format: `distance(latitude,longitude,distance)`
- Distance can be in miles (mi) or kilometers (km)
- NYC coordinates: 40.7128, -74.0060
- LA coordinates: 34.0522, -118.2437
- Chicago coordinates: 41.8781, -87.6298

## Sponsor Searches

### Federal Agencies

```
Tool: search_clinical_trials
Parameters:
  query_spons: "National Institute of Mental Health"
```

**Common federal sponsors:**
- National Institute of Mental Health (NIMH)
- National Cancer Institute (NCI)
- National Heart, Lung, and Blood Institute (NHLBI)
- National Institute of Diabetes and Digestive and Kidney Diseases (NIDDK)
- National Institute on Aging (NIA)

### Pharmaceutical Companies

```
Tool: search_clinical_trials
Parameters:
  query_spons: "Pfizer"
```

### Academic Institutions

```
Tool: search_clinical_trials
Parameters:
  query_lead: "Stanford University"
```

## Advanced Searches

### Phase-Specific Trials

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Alzheimer's Disease"
  filter_advanced: "SEARCH[Study](AREA[Phase]PHASE3)"
```

### Recent Trials (Last 2 years)

```
Tool: search_clinical_trials
Parameters:
  query_cond: "COVID-19"
  filter_advanced: "SEARCH[Study](AREA[StartDate]RANGE[2023-01-01,MAX])"
```

### Large Trials (>500 participants)

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Cardiovascular Disease"
  filter_advanced: "SEARCH[Study](AREA[EnrollmentCount]RANGE[500,MAX])"
```

## Pagination

### First Page

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Breast Cancer"
  page_size: 50
  count_total: true
```

### Next Page

Use the `nextPageToken` from the previous response:

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Breast Cancer"
  page_size: 50
  page_token: "abc123xyz..."
```

## Getting Study Details

### By NCT ID

```
Tool: get_clinical_trial
Parameters:
  nct_id: "NCT04267848"
```

### Multiple Studies

Call the tool multiple times with different NCT IDs:

```
Tool: get_clinical_trial
Parameters:
  nct_id: "NCT04267848"

Tool: get_clinical_trial
Parameters:
  nct_id: "NCT03456789"
```

## Research Use Cases

### 1. Literature Review - Find All Trials for Condition

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Major Depressive Disorder"
  page_size: 100
  count_total: true
  sort: ["LastUpdatePostDate:desc"]
```

### 2. Competitive Intelligence - Company's Trials

```
Tool: search_clinical_trials
Parameters:
  query_spons: "Biogen"
  filter_overallStatus: ["RECRUITING", "ACTIVE_NOT_RECRUITING"]
```

### 3. Site Feasibility - Local Recruiting Trials

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Rheumatoid Arthritis"
  query_locn: "Philadelphia"
  filter_overallStatus: ["RECRUITING"]
```

### 4. Patient Recruitment - Matching Criteria

```
# First, search broadly
Tool: search_clinical_trials
Parameters:
  query_cond: "Type 2 Diabetes"
  query_locn: "Seattle"
  filter_overallStatus: ["RECRUITING"]

# Then get details for specific trials
Tool: get_clinical_trial
Parameters:
  nct_id: "NCT[from search]"
```

### 5. Regulatory Intelligence - Recently Completed

```
Tool: search_clinical_trials
Parameters:
  query_intr: "CAR-T"
  filter_overallStatus: ["COMPLETED"]
  sort: ["CompletionDate:desc"]
```

### 6. Market Research - Pipeline Analysis

```
Tool: search_clinical_trials
Parameters:
  query_cond: "Alzheimer's Disease"
  filter_overallStatus: ["RECRUITING", "ACTIVE_NOT_RECRUITING"]
  sort: ["@relevance"]
  page_size: 100
```

## Statistics

### Overall Trial Statistics

```
Tool: get_trial_statistics
Parameters: {}
```

### Status Distribution

```
Tool: get_trial_statistics
Parameters:
  filter_overallStatus: ["RECRUITING"]
```

### Geographic Distribution

```
Tool: get_trial_statistics
Parameters:
  filter_geo: "distance(40.7,-74,100mi)"
```

## Tips and Best Practices

### 1. Start Broad, Then Narrow

```
# Step 1: Broad search
query_cond: "Cancer"

# Step 2: Add specificity
query_cond: "Lung Cancer"
filter_overallStatus: ["RECRUITING"]

# Step 3: Add location
query_cond: "Lung Cancer"
filter_overallStatus: ["RECRUITING"]
query_locn: "California"
```

### 2. Use Alternative Terms

Try different terminology:
- "Depression" vs "Major Depressive Disorder" vs "MDD"
- "Heart Attack" vs "Myocardial Infarction" vs "MI"
- "Stroke" vs "Cerebrovascular Accident" vs "CVA"

### 3. Check Patient-Friendly Search

```
Tool: search_clinical_trials
Parameters:
  query_patient: "heart disease"
```

### 4. Verify with Multiple Searches

Cross-reference results:
```
# Search 1: By condition
query_cond: "Parkinson's Disease"

# Search 2: By intervention
query_intr: "Levodopa"

# Search 3: By sponsor
query_spons: "Michael J Fox Foundation"
```

### 5. Use Page Tokens for Large Datasets

```
# Always set count_total on first request
count_total: true
page_size: 100

# Use returned page_token for subsequent requests
page_token: "[token from previous response]"
```

## Common Gotchas

1. **NCT IDs**: Must include "NCT" prefix (e.g., "NCT04267848", not "04267848")

2. **Status values**: Must be exact (e.g., "RECRUITING" not "recruiting")

3. **Geographic search**: Requires exact format `distance(lat,lon,distance)`

4. **Pagination**: Must use same search parameters when using page_token

5. **Timeout**: Default is 30 seconds - complex searches may timeout

6. **Result limits**: Maximum page_size is 1000

## Error Messages

### "No studies found"
- Try broader search terms
- Remove filters
- Check spelling

### "Invalid status value"
- Use exact status names from the list above
- Status values are case-sensitive

### "Invalid NCT ID"
- Must start with "NCT"
- Must be exactly 8 digits after NCT
- Example: NCT04267848

### "Geographic filter error"
- Check format: `distance(lat,lon,distance)`
- Latitude: -90 to 90
- Longitude: -180 to 180
- Distance must include unit (mi or km)

## Resources

- [ClinicalTrials.gov Search Tips](https://clinicaltrials.gov/search/about)
- [Study Record Structure](https://clinicaltrials.gov/data-api/about-api/study-data-structure)
- [Full API Documentation](https://clinicaltrials.gov/data-api/api)
