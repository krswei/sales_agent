from google.adk.agents import Agent
from .tools import image_ocr_tool

text_from_image_agent = Agent(
    name="text_from_image_agent",
    model="gemini-2.5-flash",
    instruction="""
    Your SOLE purpose is to use the `image_ocr_tool` once.

        --- STRICT RULES ---
        1. Always call the `image_ocr_tool`.
        2. The `image_ocr_tool` will return results as a JSON dictionary or an error message.
        3. It is okay if the `image_ocr_tool` returns an empty JSON dictionary. Do not call the `image_ocr_tool` again.
        4. Your final response MUST be ONLY the exact output returned by the `image_ocr_tool`.
        5. Do NOT add any introductory text, explanation, or conversational filler.
        --- END STRICT RULES ---

        Must useo tool:
        image_ocr_tool: Extracts text from images.
    """,
    description="Extracts text from uploaded images.",
    tools=[image_ocr_tool],
)
