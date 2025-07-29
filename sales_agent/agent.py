from google.adk.runners import Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions import InMemorySessionService

from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent
from google.adk.agents.callback_context import CallbackContext
import google.genai.types as types
from nanoid import generate

from .subagents.text_from_image_agent import text_from_image_agent
from .subagents.csv_parser_agent import csv_parser_agent
from .subagents.text_from_pdf_agent import text_from_pdf_agent

from .subagents.costco_report_agent import costco_report_agent
from .subagents.costco_estimate_agent import costco_estimate_agent
from .subagents.costco_membership_agent import costco_membership_agent

from .subagents.estimate_reviewer_agent import estimate_reviewer_agent
from .subagents.estimate_refiner_agent import estimate_refiner_agent

from .subagents.pitch_agent import pitch_agent

# Before-agent callback to process uploaded files and store artifact filenames in session state
async def process_uploaded_file_callback(callback_context: CallbackContext):
    """
    This callback saves uploaded files directly as artifacts and stores image, PDF, and CSV artifact filenames in the session state.
    """
    # Check if user_content has file parts
    if callback_context.user_content and getattr(callback_context.user_content, "parts", None):
        parts = getattr(callback_context.user_content, "parts", None)
        # Retrieve or initialize artifact filename lists from session state
        image_artifact_filenames = callback_context.state.get('image_artifact_filenames', [])
        pdf_artifact_filenames = callback_context.state.get('pdf_artifact_filenames', [])
        csv_artifact_filenames = callback_context.state.get('csv_artifact_filenames', [])
        if parts:
            for part in parts:
                # Only process valid Part objects with inline data
                if isinstance(part, types.Part) and part.inline_data and part.inline_data.data:
                    id = generate(size=8)  # Generate unique ID for filename fallback
                    filename = getattr(part.inline_data, 'display_name', None) or f"{id}"
                    mime_type = part.inline_data.mime_type
                    try:
                        # Save artifact using callback context
                        result = await callback_context.save_artifact(filename=filename, artifact=part)
                        print(f"Artifact save result: {result}")
                    except Exception as e:
                        print(f"Error saving artifact: {e}")
                    # Categorize artifact by MIME type
                    if mime_type:
                        if mime_type.startswith("image/"):
                            image_artifact_filenames.append(filename)
                        elif mime_type == "application/pdf":
                            pdf_artifact_filenames.append(filename)
                        elif mime_type in ["text/csv", "application/vnd.ms-excel"]:
                            csv_artifact_filenames.append(filename)
                    print(f"Saved uploaded file as artifact: {filename} ({mime_type})")
        # Update session state with artifact filenames
        callback_context.state['image_artifact_filenames'] = image_artifact_filenames
        callback_context.state['pdf_artifact_filenames'] = pdf_artifact_filenames
        callback_context.state['csv_artifact_filenames'] = csv_artifact_filenames
        # Reset parsed/processed artifact state
        callback_context.state['csv_artifacts_parsed'] = {}
        callback_context.state['image_artifact_texts'] = {}
        callback_context.state['pdf_artifact_texts'] = {}
        print("All artifacts in session:", getattr(callback_context, 'artifacts', {}))

# Agent to process uploaded files (images, PDFs, CSVs) in parallel
file_processing_agent = ParallelAgent(
    name="file_processing_agent",
    sub_agents=[csv_parser_agent, text_from_image_agent, text_from_pdf_agent],
    description="Processes uploaded files: extracts text from images and PDFs, and parses CSVs.",
)

# Agent to iteratively review and refine Costco estimates
estimate_refinement_loop_agent = LoopAgent(
    name="estimate_refinement_loop_agent",
    max_iterations=2,
    sub_agents=[estimate_reviewer_agent, estimate_refiner_agent],
    description="Iteratively reviews and refines a Costco estimate until quality requirements are met",
)

# Root agent: orchestrates file processing, report generation, estimate, membership, and pitch
root_agent = SequentialAgent(
    name="sales_agent",
    sub_agents=[file_processing_agent, costco_report_agent, costco_estimate_agent, costco_membership_agent, estimate_refinement_loop_agent, pitch_agent],
    before_agent_callback=process_uploaded_file_callback,
)

# In-memory services for artifacts and sessions
artifact_service = InMemoryArtifactService()
session_service = InMemorySessionService()

# Runner to execute the root agent
runner = Runner(
    agent=root_agent,
    app_name="varnish_sales_app",
    session_service=session_service,
    artifact_service=artifact_service,
)

print("Runner initialized.")

# Entry point (not used in this module)
if __name__ == "__main__":
    pass