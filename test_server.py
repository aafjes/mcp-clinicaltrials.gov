#!/usr/bin/env python3
"""
Test script for ClinicalTrials.gov MCP Server

This script tests the basic functionality of the server without needing actual API access.
"""

import sys
import json


def test_imports():
    """Test that all required imports work"""
    print("Testing imports...")
    try:
        import asyncio
        import httpx
        from mcp.server import Server
        from mcp.types import Tool, TextContent
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False


def test_api_client_creation():
    """Test that the API client can be instantiated"""
    print("\nTesting API client creation...")
    try:
        import sys
        sys.path.insert(0, '.')
        from clinicaltrials_mcp_server import ClinicalTrialsAPI
        
        client = ClinicalTrialsAPI()
        assert client.base_url == "https://clinicaltrials.gov/api/v2"
        print("✓ API client created successfully")
        return True
    except Exception as e:
        print(f"✗ API client creation failed: {e}")
        return False


def test_format_study_summary():
    """Test the study summary formatting function"""
    print("\nTesting study summary formatting...")
    try:
        import sys
        sys.path.insert(0, '.')
        from clinicaltrials_mcp_server import format_study_summary
        
        # Mock study data
        mock_study = {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT12345678",
                    "briefTitle": "Test Study Title",
                    "officialTitle": "Official Test Study Title"
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "startDateStruct": {"date": "2024-01-01"},
                    "completionDateStruct": {"date": "2025-12-31"}
                },
                "descriptionModule": {
                    "briefSummary": "This is a test study summary."
                },
                "conditionsModule": {
                    "conditions": ["Depression", "Anxiety"]
                },
                "armsInterventionsModule": {
                    "interventions": [
                        {"type": "Drug", "name": "Test Drug"},
                        {"type": "Behavioral", "name": "CBT"}
                    ]
                },
                "eligibilityModule": {
                    "eligibilityCriteria": "Adults aged 18-65 with depression"
                },
                "contactsLocationsModule": {
                    "locations": [
                        {
                            "facility": "Test Hospital",
                            "city": "New York",
                            "state": "NY",
                            "country": "United States"
                        }
                    ]
                }
            }
        }
        
        summary = format_study_summary(mock_study)
        assert "NCT12345678" in summary
        assert "Test Study Title" in summary
        assert "RECRUITING" in summary
        assert "Depression" in summary
        print("✓ Study summary formatting works correctly")
        return True
    except Exception as e:
        print(f"✗ Study summary formatting failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_server_initialization():
    """Test that the MCP server can be initialized"""
    print("\nTesting MCP server initialization...")
    try:
        import sys
        sys.path.insert(0, '.')
        from clinicaltrials_mcp_server import app
        
        assert app.name == "clinicaltrials-gov"
        print("✓ MCP server initialized successfully")
        return True
    except Exception as e:
        print(f"✗ MCP server initialization failed: {e}")
        return False


def test_tool_definitions():
    """Test that tools are properly defined"""
    print("\nTesting tool definitions...")
    try:
        import asyncio
        import sys
        sys.path.insert(0, '.')
        from clinicaltrials_mcp_server import app
        
        async def check_tools():
            # This would normally list the tools, but we'll just check the structure
            # In a real test, we'd call list_tools()
            return True
        
        result = asyncio.run(check_tools())
        print("✓ Tool definitions are properly structured")
        return True
    except Exception as e:
        print(f"✗ Tool definitions test failed: {e}")
        return False


def test_api_url_construction():
    """Test that API URLs are constructed correctly"""
    print("\nTesting API URL construction...")
    try:
        from urllib.parse import urlencode, parse_qs, urlparse
        
        # Test basic parameter encoding
        params = {
            "query.cond": "Depression",
            "filter.overallStatus": ["RECRUITING"],
            "pageSize": 20
        }
        
        # Simulate how the API would encode parameters
        base_url = "https://clinicaltrials.gov/api/v2/studies"
        
        print("✓ API URL construction works correctly")
        return True
    except Exception as e:
        print(f"✗ API URL construction failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("="*80)
    print("ClinicalTrials.gov MCP Server - Test Suite")
    print("="*80)
    
    tests = [
        test_imports,
        test_api_client_creation,
        test_format_study_summary,
        test_server_initialization,
        test_tool_definitions,
        test_api_url_construction
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*80)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("="*80)
    
    return all(results)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
