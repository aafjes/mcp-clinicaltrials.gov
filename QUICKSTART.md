# Quick Start Guide - ClinicalTrials.gov MCP Server

Get up and running in 5 minutes.

## Prerequisites

✓ Python 3.10 or higher  
✓ pip package manager  
✓ Claude Desktop (optional, for Claude integration)

## Installation

### Step 1: Install Dependencies

```bash
pip install mcp httpx pydantic
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Test the Server

```bash
python3 test_server.py
```

You should see:
```
Testing imports...
✓ All imports successful
Testing API client creation...
✓ API client created successfully
...
Test Results: 6/6 passed
```

## Setup for Claude Desktop

### macOS

1. **Find your config file:**
   ```bash
   open ~/Library/Application\ Support/Claude/
   ```

2. **Edit `claude_desktop_config.json`:**
   ```json
   {
     "mcpServers": {
       "clinicaltrials": {
         "command": "python3",
         "args": ["/FULL/PATH/TO/clinicaltrials_mcp_server.py"]
       }
     }
   }
   ```

3. **Replace `/FULL/PATH/TO/` with actual path:**
   ```bash
   # Get the full path
   cd /path/to/downloaded/files
   pwd
   # Copy that path and use it in the config
   ```

4. **Restart Claude Desktop**

### Windows

1. **Find your config file:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Edit the file:**
   ```json
   {
     "mcpServers": {
       "clinicaltrials": {
         "command": "python",
         "args": ["C:\\Full\\Path\\To\\clinicaltrials_mcp_server.py"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

## Verify It Works

### In Claude Desktop

Ask Claude:
```
Can you search for recruiting clinical trials about depression?
```

Claude should use the `search_clinical_trials` tool and return results.

### Testing Manually

```bash
python3 example_usage.py
```

This will run several example queries and show the results.

## Your First Queries

### Example 1: Search by Condition

Ask Claude:
```
Find recruiting clinical trials for Type 2 Diabetes
```

### Example 2: Get Trial Details

Ask Claude:
```
Get details for clinical trial NCT04267848
```

### Example 3: Search by Location

Ask Claude:
```
Find clinical trials for anxiety in Boston that are recruiting
```

### Example 4: Search by Sponsor

Ask Claude:
```
Find trials sponsored by the National Institute of Mental Health
```

## Common Issues

### "Command not found"

**Problem:** Python not found in PATH

**Solution:**
```bash
# Find Python location
which python3  # macOS/Linux
where python   # Windows

# Use full path in config
{
  "command": "/usr/local/bin/python3",
  ...
}
```

### "Module not found"

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install mcp httpx pydantic
# Or if using virtual environment:
/path/to/venv/bin/pip install mcp httpx pydantic
```

### Server not appearing in Claude

**Problem:** Config file syntax error

**Solution:**
1. Validate JSON syntax at https://jsonlint.com
2. Check file path is absolute, not relative
3. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

### No results returned

**Problem:** Network or API access

**Solution:**
1. Test internet connection
2. Visit https://clinicaltrials.gov in browser
3. Check firewall/proxy settings

## What's Next?

### Learn More
- **README.md** - Full documentation
- **QUICK_REFERENCE.md** - Common query patterns
- **FIELD_REFERENCE.md** - All available fields
- **CONFIGURATION.md** - Advanced setup

### Try Advanced Features

1. **Pagination for large results:**
   ```
   Find all depression trials and use pagination
   ```

2. **Geographic search:**
   ```
   Find cancer trials within 50 miles of New York City
   ```

3. **Multiple filters:**
   ```
   Find recruiting Phase 3 trials for diabetes in California
   ```

4. **Get statistics:**
   ```
   Get statistics on recruiting clinical trials
   ```

## Tips for Best Results

1. **Be Specific:** "Find recruiting depression trials" is better than "Find trials"

2. **Use Medical Terms:** Both "Depression" and "Major Depressive Disorder" work

3. **Specify Status:** Add "recruiting" or "completed" to narrow results

4. **Include Location:** Add city/state/institution for local trials

5. **Ask for Details:** After finding trials, ask for "details for NCT[ID]"

## Quick Reference

### Search Parameters

| What you want | Use parameter |
|---------------|---------------|
| Search condition | query_cond: "Depression" |
| Search drug/treatment | query_intr: "Pembrolizumab" |
| Search location | query_locn: "Stanford" |
| Search sponsor | query_spons: "Pfizer" |
| Filter by status | filter_overallStatus: ["RECRUITING"] |

### Common Statuses

- **RECRUITING** - Currently enrolling
- **COMPLETED** - Study finished
- **ACTIVE_NOT_RECRUITING** - Ongoing, not enrolling
- **NOT_YET_RECRUITING** - Not yet open

### Tools Available

1. **search_clinical_trials** - Find trials by various criteria
2. **get_clinical_trial** - Get details for specific NCT ID
3. **get_trial_statistics** - Get aggregate statistics

## Example Session

```
You: Find recruiting depression trials in New York

Claude: [Uses search_clinical_trials tool]
Found 15 recruiting depression trials in New York...

You: Get details for the first one

Claude: [Uses get_clinical_trial tool]
Here are the complete details for NCT[ID]...

You: Are there any trials using ketamine?

Claude: [Uses search_clinical_trials tool with query_intr]
Found 8 trials using ketamine for depression...
```

## Getting Help

1. **Test first:** Run `python3 test_server.py`
2. **Check examples:** Run `python3 example_usage.py`
3. **Read docs:** See README.md
4. **Check logs:** Look in Claude Desktop log directory

## Support

For issues:
- Check the README.md troubleshooting section
- Verify Python and dependencies are installed
- Test the server manually
- Review Claude Desktop logs

## Security Note

- This server accesses only public ClinicalTrials.gov data
- No authentication required
- No personal data collected
- Runs locally on your machine

## Ready to Use!

You're all set! Start asking Claude about clinical trials.

Example query to try right now:
```
Find recruiting clinical trials for [your condition of interest]
```

---

**Quick Links:**
- Full Documentation: README.md
- Configuration Help: CONFIGURATION.md  
- Query Examples: QUICK_REFERENCE.md
- Field Reference: FIELD_REFERENCE.md

**Need Help?** Check the README.md troubleshooting section.
