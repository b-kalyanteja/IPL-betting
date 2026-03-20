import requests
gemini_jey = "AIzaSyAbtS8y4tL79UE_qhc6BslYJ_d32UbWYL8"

import google.generativeai as genai


system_instruction = (
    "You are a cricket match analyzer for IPL 2025 and 2026. "
    "Your ONLY task is to output the winning team's abbreviation. "
    "Valid abbreviations: [csk, mi, pbks, rcb, rr, srh, kkr, dc, gt, lsg, nr_draw]."
    "if there is not result for the match give nr_draw will be given."
    "Constraint: You must respond with exactly ONE word from the list. "
    "No punctuation, no explanations, no bolding."
)

genai.configure(api_key="AIzaSyAbtS8y4tL79UE_qhc6BslYJ_d32UbWYL8")
model = genai.GenerativeModel(model_name="gemini-2.5-flash",system_instruction=system_instruction)


def get_prediction(team_a, team_b, match_date):
    prompt = f"Match: {team_a} vs {team_b}, Date: {match_date}"

    # Temperature 0.0 ensures the output is consistent and non-creative
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(temperature=0.0)
    )

    return response.text.strip().lower()


# --- Example Usage ---
winner = get_prediction("kkr", "csk", "7/5/2025")
print({winner})