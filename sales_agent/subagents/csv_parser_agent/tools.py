from google.adk.tools.tool_context import ToolContext
import google.genai.types as types

import pandas as pd
import io
import json


async def csv_paser_tool(tool_context: ToolContext) -> str:
    """
    Parses all CSV files listed in csv_artifact_filenames in the session state.
    Stores the parsed content in session state as csv_artifacts_parsed.
    This tool MUST be used for all CSV parsing operations.
    """
    
    # Retrieve the list of CSV artifact filenames from the session state
    csv_artifact_filenames = tool_context.state.get('csv_artifact_filenames', [])
    if not csv_artifact_filenames:
        # If no filenames are provided, return a message
        return "No csv artifacts."

    parsed_csvs = {}  # Dictionary to store parsed CSV data
    for filename in csv_artifact_filenames:
        # Retrieve the artifact (file) from the context asynchronously
        artifact = await tool_context.load_artifact(filename)
        # Try to get the inline_data attribute from the artifact
        inline_data = getattr(artifact, 'inline_data', None)
        # Try to get the data attribute from inline_data (should be bytes)
        data = getattr(inline_data, 'data', None) if inline_data is not None else None
        if artifact and inline_data is not None and data is not None:
            try:
                # Assume data is bytes, decode to string
                csv_bytes = data
                csv_str = csv_bytes.decode('utf-8')
                # Parse CSV with pandas using io.StringIO
                df = pd.read_csv(io.StringIO(csv_str))
                # Store the parsed CSV as a list of dicts (records) in the result
                parsed_csvs[filename] = df.to_dict(orient='records')
            except Exception as e:
                # If parsing fails, store the error message
                parsed_csvs[filename] = {"error": str(e)}
        else:
            # If artifact or data is missing, store an error message
            parsed_csvs[filename] = {"error": "Artifact data not found or is empty"}

    # Store the parsed CSVs in the session state for later use
    tool_context.state['csv_artifacts_parsed'] = parsed_csvs

    # Return the parsed CSVs as a pretty-printed JSON string
    return json.dumps(parsed_csvs, indent=2)

