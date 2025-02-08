# llm.py

from groq import Groq
import json

def get_risk_analysis(summary):
    """
    Uses an AI model to analyze environmental risk based on extracted news summaries.
    """
    response = ""
    try:
        if summary:
            system = """
                    You are an AI assistant analyzing environmental risks.
                    Return a **valid JSON object** with the following structure:
                     Assign a **severity score (1-10)** based on real-world impact:
                        * **1-3:** Low impact (localized, minor risk)
                        * **4-6:** Moderate impact (regional, some economic/ecological effects)
                        * **7-8:** High impact (nationwide, significant damage)
                        * **9-10:** Critical impact (global catastrophe, irreversible)
                    {
                        "project_overview": "Brief explanation of the environmental topic.",
                        "risk": "Main environmental risk identified (3 words max)",
                        "key_factors": ["Factor 1", "Factor 2", "Factor 3"],
                        "key_points": ["Insight 1", "Insight 2"],
                        "severity": 1-10  # Integer between 1 (low risk) and 10 (high risk)
                    }
                    Do not return any extra text, only valid JSON.
                """

            user = f"Analyze this summary and return structured JSON:\n{summary}"
            prompt = f'{system}\n {user}'
            client = Groq(api_key="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")

            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-70b-8192"
            )
            response = chat.choices[0].message.content

            # Ensure the response is valid JSON
            return json.loads(response)  

    except Exception as e:
        print(f"Error while analyzing risk: {e}")
        return {
            "project_overview": "⚠️ No analysis available.",
            "key_factors": ["Error processing data"],
            "key_points": ["Please try again later."],
            "severity": 5
        }  # Return a default structured response

    return response



def format_risk_analysis(raw_analysis):
    """Formats AI risk analysis output into a human-readable format."""
    try:
        if not raw_analysis or not raw_analysis.strip():
            return "⚠️ No risk analysis available."

        try:
            risk_data = json.loads(raw_analysis)  # ✅ Now AI always returns JSON
        except json.JSONDecodeError:
            print("Warning: AI returned non-JSON response. Displaying raw text.")
            return f"**Risk Analysis Report**\n\n{raw_analysis}"

        formatted_text = f"**🌍 Risk Analysis Report**\n\n"

        formatted_text += f"📌 **Project Overview:**\n{risk_data.get('project_overview', 'No description available.')}\n\n"

        formatted_text += "**🔹 Key Environmental Risk Factors:**\n"
        for factor in risk_data.get("key_factors", []):
            formatted_text += f"- {factor}\n"

        formatted_text += "\n**📊 Key Insights:**\n"
        for point in risk_data.get("key_points", []):
            formatted_text += f"- {point}\n"

        formatted_text += f"\n⚠️ **Severity Level:** {risk_data.get('severity', 'N/A')} (Scale: 1-10)\n"

        return formatted_text

    except Exception as e:
        print(f"Error formatting risk analysis: {e}")
        return "⚠️ Error processing risk analysis."

if __name__ == '__main__':
    sample_summary = "Recent wildfires in California have increased air pollution levels significantly, leading to public health concerns."
    print(get_risk_analysis(sample_summary))