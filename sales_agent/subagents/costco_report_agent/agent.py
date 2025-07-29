from google.adk.agents import LlmAgent
from google.adk.tools import google_search

costco_report_agent = LlmAgent(
    name="costco_report_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a helpful assistant that synthesizes a report of Costco purchases from the parsed csvs, pdf texts, and image texts.

    Instructions:
    - Analyze {parsed_csvs} and {pdf_artifact_texts} and {image_artifact_texts} of Costco purchases.
    - Note that {parsed_csvs} and {pdf_artifact_texts} and {image_artifact_texts} are dictionaries with the results from the csv_parser_agent, text_from_image_agent, and text_from_pdf_agent.
    {parsed_csvs}, {pdf_artifact_texts}, or {image_artifact_texts} maybe empty if the user did not upload the corresponding files. This is okay.
    - If {parsed_csvs}, {pdf_artifact_texts}, and {image_artifact_texts} are all empty, return "No information found."
    - If there's no Costco information provided in {parsed_csvs}, {pdf_artifact_texts}, or {image_artifact_texts}, return "No Costco information found."
    - It is possible that the files are not receipts or not from Costco. In this case, return "No Costco information found."
    - Return a JSON object with the following structure:
        For each receipt, provide a JSON object with these keys:
        - transaction: with date, time, total_amount, subtotal, tax, instant_savings, total_items 
        - items: an array of objects, each with sku, name, price, instant_savings, taxable, and category (e.g. food, household_cleaning, personal_care_pharmacy, electronics_appliances, furniture, seasonal, clothing, travel, gasoline)
        For each non-emptycategory, provide a JSON object with the total amount spent in that category across all receipts (not per receipt).
        Wrap all receipts in a JSON array.
    - Use google search to find the category of the purchase if the category is not obvious from the information in the receipt.
    """,
    description="Synthesizes a report of Costco purchases.",
    output_key="costco_purchasing_report",
    tools=[google_search],
)
