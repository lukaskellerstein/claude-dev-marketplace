#!/usr/bin/env python3
"""
Documentation Index MCP Server
Provides curated documentation links as MCP resources for all plugins
"""
import asyncio
import json
from pathlib import Path
from mcp.server import Server
from mcp.types import Resource
import mcp.server.stdio

# Load documentation index
DOCS_FILE = Path(__file__).parent / "docs-index.json"

def load_docs():
    """Load documentation index from JSON file"""
    with open(DOCS_FILE, 'r') as f:
        return json.load(f)

# Create server instance
app = Server("docs-index")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List all available documentation resources"""
    docs = load_docs()
    resources = []

    for category, items in docs.items():
        for item in items:
            resources.append(Resource(
                uri=f"docs://{category}/{item['id']}",
                name=item['name'],
                description=item['description'],
                mimeType="text/plain"
            ))

    return resources

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific documentation resource"""
    docs = load_docs()

    # Parse URI: docs://category/id
    parts = uri.replace("docs://", "").split("/")
    if len(parts) != 2:
        raise ValueError(f"Invalid URI format: {uri}")

    category, doc_id = parts

    # Find the document
    if category not in docs:
        raise ValueError(f"Category not found: {category}")

    for item in docs[category]:
        if item['id'] == doc_id:
            # Return formatted documentation info
            content = f"""# {item['name']}

{item['description']}

## Documentation URL
{item['url']}

## Tags
{', '.join(item.get('tags', []))}

## Related Topics
{', '.join(item.get('related', []))}
"""
            return content

    raise ValueError(f"Document not found: {doc_id} in {category}")

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
