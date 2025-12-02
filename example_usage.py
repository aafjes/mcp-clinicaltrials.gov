#!/usr/bin/env python3
"""
Example usage of the ClinicalTrials.gov MCP Server

This script demonstrates how to use the various tools provided by the server.
"""

import asyncio
import json
from mcp.client.stdio import stdio_client
from mcp.types import CallToolRequest


async def run_examples():
    """Run example queries against the ClinicalTrials.gov MCP server"""
    
    # Connect to the server
    async with stdio_client(
        server_params={
            "command": "python",
            "args": ["clinicaltrials_mcp_server.py"]
        }
    ) as (read, write):
        
        print("="*80)
        print("ClinicalTrials.gov MCP Server - Example Usage")
        print("="*80)
        print()
        
        # Example 1: Search for depression trials
        print("Example 1: Search for recruiting depression trials")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="search_clinical_trials",
                arguments={
                    "query_cond": "Depression",
                    "filter_overallStatus": ["RECRUITING"],
                    "page_size": 5
                }
            )
        )
        print(result.content[0].text[:1000] + "...\n")
        
        # Example 2: Search for trials with specific intervention
        print("Example 2: Search for trials using Pembrolizumab for Melanoma")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="search_clinical_trials",
                arguments={
                    "query_cond": "Melanoma",
                    "query_intr": "Pembrolizumab",
                    "page_size": 3
                }
            )
        )
        print(result.content[0].text[:1000] + "...\n")
        
        # Example 3: Search by sponsor
        print("Example 3: Search for NIMH-sponsored trials")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="search_clinical_trials",
                arguments={
                    "query_spons": "National Institute of Mental Health",
                    "filter_overallStatus": ["RECRUITING"],
                    "page_size": 3
                }
            )
        )
        print(result.content[0].text[:1000] + "...\n")
        
        # Example 4: Search by location
        print("Example 4: Search for trials at Stanford")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="search_clinical_trials",
                arguments={
                    "query_locn": "Stanford",
                    "query_cond": "Anxiety",
                    "page_size": 3
                }
            )
        )
        print(result.content[0].text[:1000] + "...\n")
        
        # Example 5: Get specific trial details
        print("Example 5: Get details for a specific trial (NCT04267848)")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="get_clinical_trial",
                arguments={
                    "nct_id": "NCT04267848"
                }
            )
        )
        print(result.content[0].text[:1500] + "...\n")
        
        # Example 6: Complex search with multiple criteria
        print("Example 6: Complex search - Recruiting diabetes trials with drug interventions in California")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="search_clinical_trials",
                arguments={
                    "query_cond": "Type 2 Diabetes",
                    "query_locn": "California",
                    "filter_overallStatus": ["RECRUITING"],
                    "page_size": 5,
                    "count_total": True
                }
            )
        )
        print(result.content[0].text[:1000] + "...\n")
        
        # Example 7: Get statistics
        print("Example 7: Get statistics on recruiting trials")
        print("-"*80)
        
        result = await write.call_tool(
            CallToolRequest(
                name="get_trial_statistics",
                arguments={
                    "filter_overallStatus": ["RECRUITING"]
                }
            )
        )
        print(result.content[0].text[:800] + "...\n")
        
        print("="*80)
        print("Examples completed!")
        print("="*80)


if __name__ == "__main__":
    asyncio.run(run_examples())
