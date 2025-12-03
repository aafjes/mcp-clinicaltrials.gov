#!/usr/bin/env python3
"""
ClinicalTrials.gov MCP Server
A Model Context Protocol server for searching and retrieving clinical trial data from ClinicalTrials.gov API v2
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from urllib.parse import urlencode

import httpx
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clinicaltrials-mcp")

# API Configuration
API_BASE_URL = "https://clinicaltrials.gov/api/v2"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 1000

class ClinicalTrialsAPI:
    """Client for interacting with ClinicalTrials.gov API v2"""

    def __init__(self):
        self.base_url = API_BASE_URL
        headers = {
            "User-Agent": "ClinicalTrials-MCP-Server/1.0 (https://github.com/aafjes/mcp-clinicaltrials.gov)",
            "Accept": "application/json"
        }
        self.client = httpx.AsyncClient(timeout=30.0, headers=headers)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    async def search_studies(
        self,
        query_cond: Optional[str] = None,
        query_term: Optional[str] = None,
        query_intr: Optional[str] = None,
        query_titles: Optional[str] = None,
        query_outc: Optional[str] = None,
        query_spons: Optional[str] = None,
        query_lead: Optional[str] = None,
        query_id: Optional[str] = None,
        query_patient: Optional[str] = None,
        query_locn: Optional[str] = None,
        filter_overallStatus: Optional[List[str]] = None,
        filter_geo: Optional[str] = None,
        filter_ids: Optional[List[str]] = None,
        filter_advanced: Optional[str] = None,
        postFilter_overallStatus: Optional[List[str]] = None,
        postFilter_geo: Optional[str] = None,
        aggFilters: Optional[str] = None,
        geoDecay: Optional[str] = None,
        fields: Optional[List[str]] = None,
        sort: Optional[List[str]] = None,
        page_size: int = DEFAULT_PAGE_SIZE,
        page_token: Optional[str] = None,
        count_total: bool = False,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Search for clinical trials using the ClinicalTrials.gov API v2
        
        Query Parameters:
        - query_cond: Search for conditions/diseases
        - query_term: Search across all study fields
        - query_intr: Search for interventions/treatments
        - query_titles: Search in study titles
        - query_outc: Search in outcome measures
        - query_spons: Search for sponsors
        - query_lead: Search for lead sponsors
        - query_id: Search by study identifiers (NCT ID)
        - query_patient: Search conditions using patient-friendly language
        - query_locn: Search by location/facility
        
        Filter Parameters:
        - filter_overallStatus: Filter by recruitment status (e.g., ["RECRUITING", "COMPLETED"])
        - filter_geo: Geographic filter (e.g., "distance(40.7,-74,50mi)")
        - filter_ids: Filter by specific NCT IDs
        - filter_advanced: Advanced query expression
        
        Other Parameters:
        - fields: List of fields to return (if not specified, returns all)
        - sort: Sort order (e.g., ["@relevance"])
        - page_size: Number of results per page (default 20, max 1000)
        - page_token: Token for pagination
        - count_total: Whether to count total results
        - format: Response format (json, csv)
        """
        
        params = {}
        
        # Add query parameters
        if query_cond:
            params["query.cond"] = query_cond
        if query_term:
            params["query.term"] = query_term
        if query_intr:
            params["query.intr"] = query_intr
        if query_titles:
            params["query.titles"] = query_titles
        if query_outc:
            params["query.outc"] = query_outc
        if query_spons:
            params["query.spons"] = query_spons
        if query_lead:
            params["query.lead"] = query_lead
        if query_id:
            params["query.id"] = query_id
        if query_patient:
            params["query.patient"] = query_patient
        if query_locn:
            params["query.locn"] = query_locn
        
        # Add filter parameters
        if filter_overallStatus:
            params["filter.overallStatus"] = filter_overallStatus
        if filter_geo:
            params["filter.geo"] = filter_geo
        if filter_ids:
            params["filter.ids"] = filter_ids
        if filter_advanced:
            params["filter.advanced"] = filter_advanced
        if postFilter_overallStatus:
            params["postFilter.overallStatus"] = postFilter_overallStatus
        if postFilter_geo:
            params["postFilter.geo"] = postFilter_geo
        if aggFilters:
            params["aggFilters"] = aggFilters
        if geoDecay:
            params["geoDecay"] = geoDecay
        
        # Add fields and sorting
        if fields:
            params["fields"] = "|".join(fields)
        if sort:
            params["sort"] = sort
        
        # Add pagination
        params["pageSize"] = min(page_size, MAX_PAGE_SIZE)
        if page_token:
            params["pageToken"] = page_token
        
        # Add other options
        if count_total:
            params["countTotal"] = "true"
        params["format"] = format
        
        url = f"{self.base_url}/studies"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_study(
        self,
        nct_id: str,
        fields: Optional[List[str]] = None,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Get detailed information for a specific clinical trial by NCT ID
        
        Args:
        - nct_id: The NCT ID of the study (e.g., "NCT04267848")
        - fields: List of specific fields to return (if not specified, returns all)
        - format: Response format (json, csv)
        """
        
        params = {"format": format}
        
        if fields:
            params["fields"] = "|".join(fields)
        
        url = f"{self.base_url}/studies/{nct_id}"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    
    async def get_study_statistics(
        self,
        filter_overallStatus: Optional[List[str]] = None,
        filter_geo: Optional[str] = None,
        agg_filters: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get aggregate statistics about clinical trials
        
        Args:
        - filter_overallStatus: Filter by recruitment status
        - filter_geo: Geographic filter
        - agg_filters: Aggregation filter expression
        """
        
        params = {}
        
        if filter_overallStatus:
            params["filter.overallStatus"] = filter_overallStatus
        if filter_geo:
            params["filter.geo"] = filter_geo
        if agg_filters:
            params["aggFilters"] = agg_filters
        
        url = f"{self.base_url}/stats"
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        return response.json()


def format_study_summary(study: Dict[str, Any]) -> str:
    """Format a study record into a readable summary"""
    
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    description = protocol.get("descriptionModule", {})
    conditions = protocol.get("conditionsModule", {})
    interventions = protocol.get("armsInterventionsModule", {})
    eligibility = protocol.get("eligibilityModule", {})
    contacts = protocol.get("contactsLocationsModule", {})
    
    summary = []
    
    # Basic identification
    summary.append(f"NCT ID: {identification.get('nctId', 'N/A')}")
    summary.append(f"Title: {identification.get('briefTitle', 'N/A')}")
    summary.append(f"Official Title: {identification.get('officialTitle', 'N/A')}")
    summary.append("")
    
    # Status
    summary.append(f"Overall Status: {status.get('overallStatus', 'N/A')}")
    summary.append(f"Study Start Date: {status.get('startDateStruct', {}).get('date', 'N/A')}")
    summary.append(f"Completion Date: {status.get('completionDateStruct', {}).get('date', 'N/A')}")
    summary.append("")
    
    # Description
    if description.get('briefSummary'):
        summary.append(f"Brief Summary: {description['briefSummary']}")
        summary.append("")
    
    # Conditions
    if conditions.get('conditions'):
        summary.append(f"Conditions: {', '.join(conditions['conditions'])}")
        summary.append("")
    
    # Interventions
    if interventions.get('interventions'):
        summary.append("Interventions:")
        for intervention in interventions['interventions'][:5]:  # Limit to first 5
            summary.append(f"  - {intervention.get('type', 'N/A')}: {intervention.get('name', 'N/A')}")
        summary.append("")
    
    # Eligibility
    if eligibility.get('eligibilityCriteria'):
        summary.append("Eligibility Criteria:")
        criteria = eligibility['eligibilityCriteria']
        # Truncate if too long
        if len(criteria) > 500:
            criteria = criteria[:500] + "..."
        summary.append(criteria)
        summary.append("")
    
    # Contact locations
    if contacts.get('locations'):
        summary.append(f"Number of Locations: {len(contacts['locations'])}")
        # Show first few locations
        for location in contacts['locations'][:3]:
            facility = location.get('facility', 'N/A')
            city = location.get('city', 'N/A')
            state = location.get('state', '')
            country = location.get('country', 'N/A')
            location_str = f"{facility}, {city}"
            if state:
                location_str += f", {state}"
            location_str += f", {country}"
            summary.append(f"  - {location_str}")
        if len(contacts.get('locations', [])) > 3:
            summary.append(f"  ... and {len(contacts['locations']) - 3} more locations")
        summary.append("")
    
    return "\n".join(summary)


# Initialize the MCP server
app = Server("clinicaltrials-gov")
api_client = ClinicalTrialsAPI()


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools"""
    return [
        Tool(
            name="search_clinical_trials",
            description="""Search for clinical trials in the ClinicalTrials.gov database. 
            
            This tool allows you to search across multiple fields including conditions, interventions, 
            sponsors, locations, and more. You can combine multiple search parameters to narrow results.
            
            Common search scenarios:
            - Search by condition: Use query_cond (e.g., "Depression", "Breast Cancer")
            - Search by intervention/drug: Use query_intr (e.g., "Pembrolizumab", "CBT")
            - Search by location: Use query_locn (e.g., "New York", "Stanford")
            - Search everything: Use query_term for general search
            - Filter by status: Use filter_overallStatus (e.g., ["RECRUITING"])
            
            Results include NCT ID, title, status, conditions, interventions, and eligibility info.
            Use page_token from results to paginate through additional results.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "query_cond": {
                        "type": "string",
                        "description": "Search for specific conditions or diseases (e.g., 'Depression', 'Type 2 Diabetes')"
                    },
                    "query_term": {
                        "type": "string",
                        "description": "Search across all study fields with keywords"
                    },
                    "query_intr": {
                        "type": "string",
                        "description": "Search for specific interventions or treatments (e.g., 'Pembrolizumab', 'Cognitive Behavioral Therapy')"
                    },
                    "query_titles": {
                        "type": "string",
                        "description": "Search within study titles"
                    },
                    "query_outc": {
                        "type": "string",
                        "description": "Search in outcome measures"
                    },
                    "query_spons": {
                        "type": "string",
                        "description": "Search for sponsors (e.g., 'Pfizer', 'National Institute of Mental Health')"
                    },
                    "query_lead": {
                        "type": "string",
                        "description": "Search for lead sponsors"
                    },
                    "query_id": {
                        "type": "string",
                        "description": "Search by study identifiers (NCT ID)"
                    },
                    "query_patient": {
                        "type": "string",
                        "description": "Search conditions using patient-friendly language"
                    },
                    "query_locn": {
                        "type": "string",
                        "description": "Search by location/facility (e.g., 'New York', 'Mayo Clinic')"
                    },
                    "filter_overallStatus": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter by recruitment status. Options: RECRUITING, NOT_YET_RECRUITING, ACTIVE_NOT_RECRUITING, COMPLETED, SUSPENDED, TERMINATED, WITHDRAWN, ENROLLING_BY_INVITATION, AVAILABLE, NO_LONGER_AVAILABLE, APPROVED_FOR_MARKETING, WITHHELD, TEMPORARILY_NOT_AVAILABLE"
                    },
                    "filter_geo": {
                        "type": "string",
                        "description": "Geographic filter using distance formula (e.g., 'distance(40.7,-74,50mi)' for studies within 50 miles of NYC)"
                    },
                    "filter_advanced": {
                        "type": "string",
                        "description": "Advanced filter expression for complex queries"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of results to return (default 20, max 1000)",
                        "default": 20
                    },
                    "page_token": {
                        "type": "string",
                        "description": "Token for pagination (from previous results)"
                    },
                    "count_total": {
                        "type": "boolean",
                        "description": "Whether to include total count of matching studies",
                        "default": False
                    },
                    "sort": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sort order (e.g., ['@relevance'], ['LastUpdatePostDate:desc'])"
                    }
                }
            }
        ),
        Tool(
            name="get_clinical_trial",
            description="""Get detailed information about a specific clinical trial by its NCT ID.
            
            This retrieves the complete record for a single study, including:
            - Full protocol information
            - Detailed eligibility criteria
            - Complete intervention details
            - All outcome measures
            - Contact information and locations
            - Study design and methodology
            - Results (if available)
            
            Use this after finding a study of interest via search to get comprehensive details.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "nct_id": {
                        "type": "string",
                        "description": "The NCT ID of the study (e.g., 'NCT04267848')"
                    },
                    "fields": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional: Specific fields to return (if not specified, returns all fields)"
                    }
                },
                "required": ["nct_id"]
            }
        ),
        Tool(
            name="get_trial_statistics",
            description="""Get aggregate statistics about clinical trials in the database.
            
            This provides summary statistics and counts across different dimensions:
            - Total number of studies
            - Distribution by status
            - Geographic distribution
            - Trends over time
            
            Useful for understanding the overall landscape of clinical research in a particular area.
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "filter_overallStatus": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter statistics by recruitment status"
                    },
                    "filter_geo": {
                        "type": "string",
                        "description": "Geographic filter for statistics"
                    },
                    "agg_filters": {
                        "type": "string",
                        "description": "Aggregation filter expression"
                    }
                }
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    """Handle tool calls"""
    
    try:
        if name == "search_clinical_trials":
            # Extract parameters
            query_cond = arguments.get("query_cond")
            query_term = arguments.get("query_term")
            query_intr = arguments.get("query_intr")
            query_titles = arguments.get("query_titles")
            query_outc = arguments.get("query_outc")
            query_spons = arguments.get("query_spons")
            query_lead = arguments.get("query_lead")
            query_id = arguments.get("query_id")
            query_patient = arguments.get("query_patient")
            query_locn = arguments.get("query_locn")
            filter_overallStatus = arguments.get("filter_overallStatus")
            filter_geo = arguments.get("filter_geo")
            filter_advanced = arguments.get("filter_advanced")
            page_size = arguments.get("page_size", DEFAULT_PAGE_SIZE)
            page_token = arguments.get("page_token")
            count_total = arguments.get("count_total", False)
            sort = arguments.get("sort")
            
            # Perform search
            results = await api_client.search_studies(
                query_cond=query_cond,
                query_term=query_term,
                query_intr=query_intr,
                query_titles=query_titles,
                query_outc=query_outc,
                query_spons=query_spons,
                query_lead=query_lead,
                query_id=query_id,
                query_patient=query_patient,
                query_locn=query_locn,
                filter_overallStatus=filter_overallStatus,
                filter_geo=filter_geo,
                filter_advanced=filter_advanced,
                page_size=page_size,
                page_token=page_token,
                count_total=count_total,
                sort=sort
            )
            
            # Format results
            studies = results.get("studies", [])
            next_page_token = results.get("nextPageToken")
            total_count = results.get("totalCount")
            
            output = []
            output.append(f"Found {len(studies)} studies in this page")
            if total_count:
                output.append(f"Total matching studies: {total_count}")
            if next_page_token:
                output.append(f"Next page token: {next_page_token}")
            output.append("\n" + "="*80 + "\n")
            
            for i, study in enumerate(studies, 1):
                output.append(f"Study {i}:")
                output.append(format_study_summary(study))
                output.append("="*80 + "\n")
            
            return [TextContent(type="text", text="\n".join(output))]
        
        elif name == "get_clinical_trial":
            nct_id = arguments["nct_id"]
            fields = arguments.get("fields")
            
            # Get study details
            result = await api_client.get_study(nct_id=nct_id, fields=fields)
            
            # Check if we got a valid response
            if "studies" in result and len(result["studies"]) > 0:
                study = result["studies"][0]
                output = format_study_summary(study)
                
                # Add raw JSON for detailed analysis if needed
                output += "\n\n" + "="*80 + "\n"
                output += "Full JSON Response (for detailed analysis):\n"
                output += json.dumps(study, indent=2)
                
                return [TextContent(type="text", text=output)]
            else:
                return [TextContent(type="text", text=f"No study found with NCT ID: {nct_id}")]
        
        elif name == "get_trial_statistics":
            filter_overallStatus = arguments.get("filter_overallStatus")
            filter_geo = arguments.get("filter_geo")
            agg_filters = arguments.get("agg_filters")
            
            # Get statistics
            stats = await api_client.get_study_statistics(
                filter_overallStatus=filter_overallStatus,
                filter_geo=filter_geo,
                agg_filters=agg_filters
            )
            
            # Format statistics
            output = "Clinical Trials Statistics\n"
            output += "="*80 + "\n\n"
            output += json.dumps(stats, indent=2)
            
            return [TextContent(type="text", text=output)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        logger.error(error_msg)
        return [TextContent(type="text", text=error_msg)]
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Main entry point"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
