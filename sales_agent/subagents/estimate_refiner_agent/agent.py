from google.adk.agents import LlmAgent

estimate_refiner_agent = LlmAgent(
    name="estimate_refiner_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a specialized agent for refining Costco estimates.

    Instructions:
     1. Review the {costco_membership_report} and consider each category's estimated value. 
     2. Where the explanation allows for it, make reasonable increases to the estimated value for that category. 
     Example: If the explanation mentions that an estimate is lower than average, you are encoraged to slightly increase the cateogry annual estimate.
     Example: If the explanation mentions that the spending pattern is low in this cateogry or the default expenditure was used, you are discouraged from increasing the estimate. Or should make a smaller rather than larger increase.
     Not all categories should be increased. Use the explanation to determine which categories are due for an increase.
     Incrememnts should be small. Around 10-20 more per month is reasonable if and only if the explanation allows for it.
     Remmeber, it is your job to increase the estimate, within a reasonable range.
     3. For each category you do increase, update the explanation to include a clear justification for the increase and state the new final value. 
     4. Return an updated {costco_membership_report} version with the new values. Include updates to the membership tiers information as well.

     ```json
        {
          "membership_report": {
            "annual_spending_estimate": {
              "total_estimated_annual_spend": <total_annual_estimate_from_report>,
              "categories": {
                "food": {
                  "annual_estimate": <food_annual_estimate>,
                  "notes": "<food_explanation>"
                },
                "household_cleaning": {
                  "annual_estimate": <household_cleaning_annual_estimate>,
                  "notes": "<household_cleaning_explanation>"
                },
                "personal_care_pharmacy": {
                  "annual_estimate": <personal_care_pharmacy_annual_estimate>,
                  "notes": "<personal_care_pharmacy_explanation>"
                },
                "electronics_appliances": {
                  "annual_estimate": <electronics_appliances_annual_estimate>,
                  "notes": "<electronics_appliances_explanation>"
                },
                "furniture": {
                  "annual_estimate": <furniture_annual_estimate>,
                  "notes": "<furniture_explanation>"
                },
                "seasonal": {
                  "annual_estimate": <seasonal_annual_estimate>,
                  "notes": "<seasonal_explanation>"
                },
                "clothing": {
                  "annual_estimate": <clothing_annual_estimate>,
                  "notes": "<clothing_explanation>"
                },
                "travel": {
                  "annual_estimate": <travel_annual_estimate>,
                  "notes": "<travel_explanation>"
                },
                "gasoline": {
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
    """,
    description="A specialized agent for refining Costco estimates.",
    output_key="costco_membership_report",
)