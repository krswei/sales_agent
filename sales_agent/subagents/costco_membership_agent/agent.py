from google.adk.agents import LlmAgent
from .tools import costco_membership_info_tool

costco_membership_agent = LlmAgent(
    name="costco_membership_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a specialized agent with knowledge of Costco's memberships and benefits.

    Instructions:
    - Analyze {costco_annual_estimate_report}, which is a JSON object with the user's annual estimate of Costco purchases
    - If {costco_annual_estimate_report} is empty, return "No Costco purchases found."
    - If {costco_annual_estimate_report} is not empty:
        - Use the costco_membership_info_tool to gather information about Costco's memberships and benefits.
        - Based upon the user's information purchasing patterns in {costco_annual_estimate_report}, determine the user's costs and savings under each membership tier.
        - The membership tiers are: Gold Star and Executive.
        - Note the importance of category spending patterns. (For example, gas does not receive cashback, but it is a frequent purchase.)
        - Return a JSON object in the following format, populating the values based on your analysis:

        ```json
        {
          "membership_report": {
            "annual_spending_estimate": {
              "total_estimated_annual_spend": <total_annual_estimate_from_report>,
              "categories": {
                "food": {
                  "spent_so_far": <food_spent_so_far>,
                  "annual_estimate": <food_annual_estimate>,
                  "notes": "<food_explanation>"
                },
                "household_cleaning": {
                  "spent_so_far": <household_cleaning_spent_so_far>,
                  "annual_estimate": <household_cleaning_annual_estimate>,
                  "notes": "<household_cleaning_explanation>"
                },
                "personal_care_pharmacy": {
                  "spent_so_far": <personal_care_pharmacy_spent_so_far>,
                  "annual_estimate": <personal_care_pharmacy_annual_estimate>,
                  "notes": "<personal_care_pharmacy_explanation>"
                },
                "electronics_appliances": {
                  "spent_so_far": <electronics_appliances_spent_so_far>,
                  "annual_estimate": <electronics_appliances_annual_estimate>,
                  "notes": "<electronics_appliances_explanation>"
                },
                "furniture": {
                  "spent_so_far": <furniture_spent_so_far>,
                  "annual_estimate": <furniture_annual_estimate>,
                  "notes": "<furniture_explanation>"
                },
                "seasonal": {
                  "spent_so_far": <seasonal_spent_so_far>,
                  "annual_estimate": <seasonal_annual_estimate>,
                  "notes": "<seasonal_explanation>"
                },
                "clothing": {
                  "spent_so_far": <clothing_spent_so_far>,
                  "annual_estimate": <clothing_annual_estimate>,
                  "notes": "<clothing_explanation>"
                },
                "travel": {
                  "spent_so_far": <travel_spent_so_far>,
                  "annual_estimate": <travel_annual_estimate>,
                  "notes": "<travel_explanation>"
                },
                "gasoline": {
                  "spent_so_far": <gasoline_spent_so_far>,
                  "annual_estimate": <gasoline_annual_estimate>,
                  "notes": "<gasoline_explanation_including_no_cashback_note>"
                },
              }
            },
            "membership_tiers": {
              "gold_star_membership": {
                "annual_cost": <gold_star_annual_cost>,
                "estimated_cashback_rewards": 0.00,
                "net_annual_cost": <gold_star_net_annual_cost>,
                "notes": 
              },
              "executive_membership": {
                "annual_cost": <executive_annual_cost>,
                "eligible_spend_for_cashback": <total_eligible_spend_for_cashback>,
                "estimated_cashback_rewards": <estimated_executive_cashback_rewards>,
                "net_annual_cost": <executive_net_annual_cost>,
                "notes": "<executive_membership_notes_including_cashback_explanation_and_other_benefits>"
              }
            }
          }
        }
        ```

    Tools:
    costco_membership_info_tool: A tool to gather information about Costco's memberships and benefits.
    """,
    description="A specialized agent for Costco.",
    tools=[costco_membership_info_tool],
    output_key="costco_membership_report",
)