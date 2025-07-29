from google.adk.agents import Agent
from .tools import csv_paser_tool

csv_parser_agent = Agent(
    name="csv_parser_agent",
    model="gemini-2.5-flash",
    instruction="""
        Your SOLE purpose is to use the `csv_paser_tool` once.

        --- STRICT RULES ---
        1. Always call the `csv_paser_tool`.
        2. The `csv_paser_tool` will return results as a JSON dictionary or an error message.
        3. It is okay if the `csv_paser_tool` returns an empty JSON dictionary. Do not call the `csv_paser_tool` again.
        4. Your final response MUST be ONLY the exact output returned by the `csv_paser_tool`.
        5. Do NOT add any introductory text, explanation, or conversational filler.
        --- END STRICT RULES ---

        Must useo tool:
        csv_paser_tool: Parses CSV files and returns a JSON dictionary of the extracted data.
        """,
    description="Parses CSV files.",
    tools=[csv_paser_tool],
    output_key="parsed_csvs",
)
