from google.adk.agents import Agent
from .tools import text_from_pdf_tool

text_from_pdf_agent = Agent(
    name="text_from_pdf_agent",
    model="gemini-2.5-flash",
    instruction="""
     Your SOLE purpose is to use the `text_from_pdf_tool` once.

        --- STRICT RULES ---
        1. Always call the `text_from_pdf_tool`.
        2. The `text_from_pdf_tool` will return results as a JSON dictionary or an error message.
        3. It is okay if the `text_from_pdf_tool` returns an empty JSON dictionary. Do not call the `text_from_pdf_tool` again.
        4. Your final response MUST be ONLY the exact output returned by the `text_from_pdf_tool`.
        5. Do NOT add any introductory text, explanation, or conversational filler.
        --- END STRICT RULES ---

        Must useo tool:
        text_from_pdf_tool: Extracts text from PDF files.
    """,
    description="Extracts text from PDF files.",
    tools=[text_from_pdf_tool],
)
