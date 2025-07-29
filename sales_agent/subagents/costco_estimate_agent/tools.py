from google.adk.tools.tool_context import ToolContext
import google.genai.types as types
import json
import os

async def costco_default_expenditure_tool(tool_context: ToolContext) -> dict:
    """
    Loads and returns Costco default expenditure information from expenditure_defaults.json.
    """
    json_path = os.path.join(os.path.dirname(__file__), 'expenditure_defaults.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data