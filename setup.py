from setuptools import setup, find_packages

setup(
    name="clinicaltrials-mcp-server",
    version="1.0.0",
    description="Model Context Protocol server for ClinicalTrials.gov API",
    author="Deliberate AI",
    python_requires=">=3.10",
    py_modules=["clinicaltrials_mcp_server"],
    install_requires=[
        "mcp>=1.0.0",
        "httpx>=0.27.0",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "clinicaltrials-mcp=clinicaltrials_mcp_server:main",
        ],
    },
)
