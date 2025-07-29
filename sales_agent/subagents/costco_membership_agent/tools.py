from google.adk.tools.tool_context import ToolContext
import google.genai.types as types
import json
import os

async def costco_membership_info_tool(tool_context: ToolContext) -> dict:
    """
    Loads and returns Costco membership tiers information from memberships.json.
    """
    json_path = os.path.join(os.path.dirname(__file__), 'memberships.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data