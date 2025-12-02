# ClinicalTrials.gov MCP Server - Project Summary

## Overview

This is a comprehensive Model Context Protocol (MCP) server that provides Claude and other AI assistants with access to the ClinicalTrials.gov database containing information about 400,000+ clinical studies worldwide.

## What's Included

### Core Implementation
- **clinicaltrials_mcp_server.py** (23KB) - Main MCP server with full API implementation
  - Search studies with multiple query parameters
  - Get detailed study information by NCT ID
  - Retrieve aggregate statistics
  - Pagination support for large result sets
  - Comprehensive error handling

### Documentation
- **README.md** (8.1KB) - Complete project documentation
  - Installation instructions
  - Configuration guide
  - Tool descriptions
  - Common use cases
  - Troubleshooting guide

- **CONFIGURATION.md** (6.8KB) - Detailed setup instructions
  - Claude Desktop configuration (macOS/Windows)
  - VS Code Cline extension setup
  - Continue.dev integration
  - Custom MCP client examples
  - Environment variables
  - Production deployment

- **QUICK_REFERENCE.md** (8.0KB) - Fast lookup guide
  - Common search patterns
  - Status filtering examples
  - Location-based searches
  - Research use cases
  - Tips and best practices
  - Common error messages

- **FIELD_REFERENCE.md** (12KB) - Complete API field documentation
  - Full study data structure
  - All available fields and modules
  - Enumeration values
  - Field selection examples
  - Date formats

### Testing & Examples
- **test_server.py** (5.9KB) - Test suite for validation
  - Import tests
  - API client tests
  - Formatting tests
  - Server initialization tests

- **example_usage.py** (4.5KB) - Working examples
  - Basic condition searches
  - Intervention searches
  - Sponsor searches
  - Location searches
  - Complex multi-criteria searches

### Setup Files
- **requirements.txt** (41 bytes) - Python dependencies
- **setup.py** (528 bytes) - Package installation script
- **LICENSE** (1.4KB) - MIT License
- **.gitignore** - Git ignore rules

## Key Features

### 1. Comprehensive Search Capabilities
- Search by condition/disease
- Search by intervention/treatment
- Search by sponsor/organization
- Search by location/facility
- Geographic radius searches
- Multiple filter combinations
- Pagination for large result sets

### 2. Detailed Study Information
Retrieve complete study records including:
- Protocol information
- Eligibility criteria
- Intervention details
- Outcome measures
- Contact information
- Study locations
- Results (when available)

### 3. Status Filtering
Filter by recruitment status:
- RECRUITING
- COMPLETED
- ACTIVE_NOT_RECRUITING
- And 10+ other statuses

### 4. Advanced Features
- Aggregate statistics
- Sort by relevance, date, or other fields
- Field selection for optimized responses
- Total count tracking
- Geographic filtering with radius

## Technical Details

### Architecture
- Built with Model Context Protocol (MCP) standard
- Uses stdio transport for communication
- Async/await pattern for efficiency
- HTTP client with timeout handling
- Structured error handling

### Dependencies
- `mcp>=1.0.0` - Model Context Protocol framework
- `httpx>=0.27.0` - Modern async HTTP client
- `pydantic>=2.0.0` - Data validation

### API Integration
- ClinicalTrials.gov API v2
- RESTful endpoints
- JSON response format
- No authentication required (public data)
- OpenAPI 3.0 specification

## Use Cases

### 1. Clinical Research
- Literature reviews
- Competitive intelligence
- Pipeline analysis
- Regulatory research

### 2. Patient Recruitment
- Finding eligible trials
- Location-based matching
- Inclusion/exclusion criteria review

### 3. Site Feasibility
- Local trial opportunities
- Sponsor analysis
- Geographic distribution

### 4. Market Intelligence
- Drug development tracking
- Sponsor activity monitoring
- Therapeutic area trends

## Integration Examples

### Claude Desktop
```json
{
  "mcpServers": {
    "clinicaltrials": {
      "command": "python3",
      "args": ["/path/to/clinicaltrials_mcp_server.py"]
    }
  }
}
```

### Python Client
```python
from mcp.client.stdio import stdio_client

async with stdio_client(server_params={...}) as (read, write):
    result = await write.call_tool(...)
```

## Example Queries

### Find recruiting depression trials
```
Tool: search_clinical_trials
Parameters:
  query_cond: "Depression"
  filter_overallStatus: ["RECRUITING"]
```

### Get trial details
```
Tool: get_clinical_trial
Parameters:
  nct_id: "NCT04267848"
```

### Local trials search
```
Tool: search_clinical_trials
Parameters:
  query_cond: "Type 2 Diabetes"
  query_locn: "Boston"
  filter_overallStatus: ["RECRUITING"]
```

## Data Access

### What You Can Search
- Medical conditions
- Interventions/treatments
- Sponsors and collaborators
- Study locations
- Study identifiers (NCT IDs)
- Outcome measures
- Study status

### What You Get Back
- Study identification (NCT ID, title)
- Status and dates
- Conditions being studied
- Interventions being tested
- Eligibility criteria
- Study locations and contacts
- Design and methodology
- Results (when posted)

## Limitations

1. **Rate Limiting**: No official limits but reasonable use expected
2. **Data Freshness**: Studies updated by sponsors/investigators
3. **Network Required**: Must access clinicaltrials.gov
4. **Result Size**: Max 1000 results per page
5. **Timeout**: 30 second default per request

## Best Practices

1. **Start Broad**: Begin with general searches, then narrow
2. **Use Filters**: Apply status filters to reduce results
3. **Paginate Large Sets**: Use page tokens for >1000 results
4. **Try Alternative Terms**: Use different medical terminology
5. **Check Multiple Fields**: Search conditions, interventions, sponsors

## Data Quality Notes

- Studies are self-reported by sponsors/investigators
- Data quality varies by submitter
- Some fields may be incomplete
- Results availability varies
- Updates depend on sponsor maintenance

## Security & Privacy

- All data is public (from ClinicalTrials.gov)
- No personal health information (PHI)
- No authentication required
- Local execution only
- No data sent to third parties

## Support & Resources

### Getting Help
1. Check README.md for general documentation
2. Review CONFIGURATION.md for setup issues
3. See QUICK_REFERENCE.md for query patterns
4. Run test_server.py to validate installation
5. Check example_usage.py for working examples

### External Resources
- [ClinicalTrials.gov](https://clinicaltrials.gov)
- [API Documentation](https://clinicaltrials.gov/data-api/api)
- [MCP Specification](https://spec.modelcontextprotocol.io/)

## Changelog

### Version 1.0.0 (2025-12-02)
- Initial release
- Full ClinicalTrials.gov API v2 support
- Three tools: search, get details, statistics
- Comprehensive documentation
- Example code and tests
- MIT License

## Future Enhancements (Potential)

- Caching layer for frequently accessed studies
- Batch study retrieval
- CSV export functionality
- Advanced filtering UI
- Result ranking/scoring
- Integration with other biomedical databases
- Study comparison features

## Contributing

This project welcomes contributions:
- Bug reports and fixes
- Documentation improvements
- Feature requests
- Code optimizations
- Test coverage expansion

## License

MIT License - See LICENSE file for full text.

Note: Users must comply with ClinicalTrials.gov Terms and Conditions when accessing data.

## Acknowledgments

- Built for Deliberate AI clinical research applications
- Uses the public ClinicalTrials.gov API
- Follows Model Context Protocol specification
- Thanks to the clinical research community

---

**Project Status**: Production Ready ✓

**Tested With**: 
- Python 3.10+
- Claude Desktop (macOS/Windows)
- MCP SDK 1.0+

**Maintained By**: Deliberate AI
**Created**: December 2, 2025
