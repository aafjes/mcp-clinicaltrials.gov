# ClinicalTrials.gov MCP Server

A Model Context Protocol (MCP) server that provides access to the ClinicalTrials.gov database, enabling Claude and other AI assistants to search and retrieve information about clinical trials.

## Overview

This MCP server implements the ClinicalTrials.gov API v2, providing comprehensive access to information about clinical studies registered in the United States and internationally. The database contains over 400,000 clinical trials from 220+ countries.

## Features

- **Comprehensive Search**: Search clinical trials by:
  - Medical conditions/diseases
  - Interventions/treatments
  - Sponsors and investigators
  - Geographic location
  - Study status (recruiting, completed, etc.)
  - NCT identifiers
  
- **Detailed Study Information**: Retrieve complete study records including:
  - Protocol information
  - Eligibility criteria
  - Intervention details
  - Outcome measures
  - Contact information and locations
  - Study design and methodology
  - Results (when available)

- **Aggregate Statistics**: Get summary statistics and trends across clinical trials

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Install from source

```bash
# Clone or download the server files
git clone <repository-url>
cd clinicaltrials-mcp-server

# Install dependencies
pip install -r requirements.txt

# Or install the package
pip install -e .
```

## Configuration

### For Claude Desktop

Add the server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "clinicaltrials": {
      "command": "python",
      "args": ["/path/to/clinicaltrials_mcp_server.py"]
    }
  }
}
```

### For other MCP clients

Use the stdio transport to connect:

```python
import asyncio
from mcp.client.stdio import stdio_client

async def main():
    async with stdio_client(
        server_params={
            "command": "python",
            "args": ["/path/to/clinicaltrials_mcp_server.py"]
        }
    ) as (read, write):
        # Use the client
        pass

asyncio.run(main())
```

## Tools

### 1. search_clinical_trials

Search for clinical trials using various criteria.

**Parameters:**

- `query_cond` (string): Search by condition/disease (e.g., "Depression", "Breast Cancer")
- `query_term` (string): General keyword search across all fields
- `query_intr` (string): Search by intervention/treatment (e.g., "Pembrolizumab", "CBT")
- `query_titles` (string): Search in study titles
- `query_outc` (string): Search in outcome measures
- `query_spons` (string): Search by sponsor name
- `query_lead` (string): Search by lead sponsor
- `query_id` (string): Search by NCT ID
- `query_patient` (string): Search using patient-friendly language
- `query_locn` (string): Search by location (e.g., "New York", "Mayo Clinic")
- `filter_overallStatus` (array): Filter by recruitment status
  - Valid values: RECRUITING, NOT_YET_RECRUITING, ACTIVE_NOT_RECRUITING, COMPLETED, SUSPENDED, TERMINATED, WITHDRAWN, ENROLLING_BY_INVITATION, AVAILABLE, NO_LONGER_AVAILABLE, APPROVED_FOR_MARKETING, WITHHELD, TEMPORARILY_NOT_AVAILABLE
- `filter_geo` (string): Geographic filter (e.g., "distance(40.7,-74,50mi)")
- `filter_advanced` (string): Advanced filter expression
- `page_size` (integer): Results per page (default 20, max 1000)
- `page_token` (string): Token for pagination
- `count_total` (boolean): Include total count of results
- `sort` (array): Sort order (e.g., ["@relevance"])

**Example Usage:**

```
Search for recruiting clinical trials about depression with cognitive behavioral therapy:
- query_cond: "Depression"
- query_intr: "Cognitive Behavioral Therapy"
- filter_overallStatus: ["RECRUITING"]
```

### 2. get_clinical_trial

Retrieve detailed information about a specific clinical trial by its NCT ID.

**Parameters:**

- `nct_id` (string, required): The NCT ID of the study (e.g., "NCT04267848")
- `fields` (array, optional): Specific fields to return (returns all if not specified)

**Example Usage:**

```
Get details for study NCT04267848:
- nct_id: "NCT04267848"
```

### 3. get_trial_statistics

Get aggregate statistics about clinical trials.

**Parameters:**

- `filter_overallStatus` (array): Filter statistics by recruitment status
- `filter_geo` (string): Geographic filter for statistics
- `agg_filters` (string): Aggregation filter expression

**Example Usage:**

```
Get statistics on recruiting trials:
- filter_overallStatus: ["RECRUITING"]
```

## Common Use Cases

### 1. Finding trials for a specific condition

```
Use search_clinical_trials with:
- query_cond: "Type 2 Diabetes"
- filter_overallStatus: ["RECRUITING"]
- page_size: 50
```

### 2. Finding trials by a specific sponsor

```
Use search_clinical_trials with:
- query_spons: "National Institute of Mental Health"
- filter_overallStatus: ["RECRUITING", "ACTIVE_NOT_RECRUITING"]
```

### 3. Finding trials in a specific location

```
Use search_clinical_trials with:
- query_cond: "Alzheimer's Disease"
- query_locn: "Stanford"
```

### 4. Finding trials with specific interventions

```
Use search_clinical_trials with:
- query_intr: "Pembrolizumab"
- query_cond: "Melanoma"
```

### 5. Getting detailed information about a trial

```
First search to find NCT IDs, then use get_clinical_trial:
- nct_id: "NCT04267848"
```

## API Details

This server uses the ClinicalTrials.gov API v2, which is a REST API with OpenAPI 3.0 specification.

**Base URL**: `https://clinicaltrials.gov/api/v2`

**Key Endpoints**:
- `/studies` - Search and list studies
- `/studies/{nctId}` - Get specific study details
- `/stats` - Get aggregate statistics

**Rate Limits**: The API does not publish specific rate limits, but reasonable use is expected. The server implements timeout handling (30 seconds per request).

## Data Structure

Study records contain multiple modules:

- **protocolSection**: Core study information
  - identificationModule: NCT ID, title, org info
  - statusModule: Recruitment status, dates
  - descriptionModule: Brief and detailed descriptions
  - conditionsModule: Conditions being studied
  - designModule: Study design details
  - armsInterventionsModule: Study arms and interventions
  - outcomesModule: Primary and secondary outcomes
  - eligibilityModule: Inclusion/exclusion criteria
  - contactsLocationsModule: Contact info and study sites
  - referencesModule: Related publications

- **resultsSection**: Study results (when available)
- **derivedSection**: Computed/derived information
- **documentSection**: Supporting documents

## Troubleshooting

### Connection Issues

If you encounter connection errors:
1. Verify internet connectivity
2. Check that the ClinicalTrials.gov API is accessible
3. Review proxy settings if behind a corporate firewall

### No Results Found

If searches return no results:
1. Try broader search terms
2. Remove filters to see all results
3. Check spelling of medical terms
4. Try alternative terminology (e.g., "MI" vs "Myocardial Infarction")

### Pagination

For large result sets:
1. Use `page_size` to control results per page (max 1000)
2. Use `page_token` from response to fetch next page
3. Set `count_total: true` to see total matching studies

## References

- [ClinicalTrials.gov Website](https://clinicaltrials.gov)
- [API Documentation](https://clinicaltrials.gov/data-api/api)
- [API Migration Guide](https://clinicaltrials.gov/data-api/about-api/api-migration)
- [Study Data Structure](https://clinicaltrials.gov/data-api/about-api/study-data-structure)

## License

This MCP server is provided as-is for accessing public data from ClinicalTrials.gov. Users must comply with [ClinicalTrials.gov Terms and Conditions](https://clinicaltrials.gov/about-site/terms-conditions).

## Support

For issues with:
- **This MCP server**: Create an issue in the repository
- **ClinicalTrials.gov API**: Contact register@clinicaltrials.gov
- **Study data questions**: Contact the study sponsor or principal investigator

## Version History

### 1.0.0 (2025-12-02)
- Initial release
- Support for ClinicalTrials.gov API v2
- Search, retrieve, and statistics tools
- Comprehensive field support
- Pagination support
