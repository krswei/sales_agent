from google.adk.tools.tool_context import ToolContext
import google.genai.types as types
from google.cloud import vision

async def image_ocr_tool(tool_context: ToolContext) -> str:
    """
    Extracts text from all image files listed in image_artifact_filenames in session state, using Google Cloud Vision OCR.
    Returns a dict mapping artifact filename to extracted text.
    This tool MUST be used for all image OCR operations.
    """
    # Get the list of image artifact filenames from the session state
    image_artifact_filenames = tool_context.state.get('image_artifact_filenames', [])
    if not image_artifact_filenames:
        # If no images are provided, return early
        return "No image artifacts."

    # Get or create the mapping of filenames to extracted text
    image_artifact_texts = tool_context.state.get('image_artifact_texts', {})

    results = []  # To store results for each image
    client = vision.ImageAnnotatorClient()  # Google Vision API client
    for filename in image_artifact_filenames:
        # Load the image artifact asynchronously
        artifact = await tool_context.load_artifact(filename)
        if not artifact or not artifact.inline_data:
            # If artifact can't be loaded, record the error
            results.append(f"[{filename}] Could not load image from artifact.")
            continue

        image_bytes = artifact.inline_data.data  # Get the image bytes

        if not image_bytes:
            # If no image data is found, record the error
            results.append(f"[{filename}] No image data found in artifact.")
            continue

        try:
            # Create a Vision API Image object
            image = vision.Image(content=image_bytes)
            # Perform text detection using Vision API
            response = client.text_detection(image=image) # type: ignore
            if response.error.message:
                # If the API returns an error, raise an exception
                raise Exception(response.error.message)
            # Extract the full text annotation if available
            extracted_text = response.full_text_annotation.text.strip() if response.full_text_annotation and response.full_text_annotation.text else 'No text found in the image.'
            # Save the extracted text in the mapping
            image_artifact_texts[filename] = extracted_text
            # Add the result to the results list
            results.append(f"[{filename}] {extracted_text}")
        except Exception as e:
            # Handle any errors during processing
            error_msg = f"Image processing failed: {e}"
            image_artifact_texts[filename] = error_msg
            results.append(f"[{filename}] {error_msg}")

    # Save the updated mapping back to the session state
    tool_context.state['image_artifact_texts'] = image_artifact_texts

    # Return a summary of the results
    return f"Artifacts saved: {image_artifact_filenames}\n\n" + "\n\n".join(results)
