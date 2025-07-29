from google.adk.tools.tool_context import ToolContext
import google.genai.types as types

import pdfplumber
import json
from io import BytesIO

async def text_from_pdf_tool(tool_context: ToolContext) -> str:
    """
    Extracts text from all pdf files listed in pdf_artifact_filenames in session state.
    Returns a JSON string mapping artifact filename to extracted text.
    Also stores the mapping in tool_context.state['pdf_artifact_texts'].
    This tool MUST be used for all PDF text extraction operations.
    """
    # Get the list of PDF artifact filenames from the tool context state
    pdf_artifact_filenames = tool_context.state.get('pdf_artifact_filenames', [])
    if not pdf_artifact_filenames:
        # If there are no PDF artifacts, return a message
        return "No pdf artifacts."

    pdf_texts = {}  # Dictionary to store extracted text for each PDF
    for filename in pdf_artifact_filenames:
        try:
            # Load the artifact asynchronously using the tool context
            artifact = await tool_context.load_artifact(filename)
            # Get the inline data attribute from the artifact (if present)
            inline_data = getattr(artifact, 'inline_data', None)
            # Get the actual binary data from the inline data (if present)
            data = getattr(inline_data, 'data', None) if inline_data is not None else None
            if artifact and inline_data is not None and data is not None:
                # Open the PDF from the binary data using pdfplumber
                with pdfplumber.open(BytesIO(data)) as pdf:
                    text = ""  # Initialize an empty string to accumulate text
                    for page in pdf.pages:
                        # Extract text from each page and append (if any)
                        text += page.extract_text() or ""
                    # Store the stripped text in the result dictionary
                    pdf_texts[filename] = text.strip()
            else:
                # If artifact or data is missing, record an error message
                error_msg = "Artifact data not found or is empty"
                pdf_texts[filename] = error_msg
        except Exception as e:
            # If any error occurs during extraction, record the error message
            error_msg = f"Error extracting text: {str(e)}"
            pdf_texts[filename] = error_msg

    # Store the mapping of filenames to extracted text in the tool context state
    tool_context.state['pdf_artifact_texts'] = pdf_texts
    # Return the mapping as a JSON string
    return json.dumps(pdf_texts, ensure_ascii=False)