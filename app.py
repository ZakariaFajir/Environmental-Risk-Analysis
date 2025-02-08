from flask import Flask, render_template, request, redirect, url_for, jsonify
from scraper import get_environmental_news
from llm import get_risk_analysis
from llm import format_risk_analysis
from visualization import plot_risk_levels
import webview
import threading
import json

app = Flask(__name__)

# Store results temporarily
search_results = {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        topic = request.form.get("topic")
        if topic:
            return redirect(url_for("loading", topic=topic))
    return render_template("home.html")

@app.route("/loading/<topic>")
def loading(topic):
    """Show the loading page while searching happens in the background."""
    return render_template("loading.html", topic=topic)

@app.route("/process/<topic>")
def process(topic):
    """Fetches news and analyzes risk while ensuring clean data."""
    news = get_environmental_news(topic)
    risks = []

    for article in news:
        if len(article["summary"]) > 50:  # Skip very short summaries
            raw_risk = get_risk_analysis(article["summary"])  # AI generates structured JSON
            risks.append({
                "project_overview": raw_risk.get("project_overview", "No overview available."),
                "risk": raw_risk.get("risk", "No risk available."),
                "key_factors": raw_risk.get("key_factors", ["No key factors identified."]),
                "key_points": raw_risk.get("key_points", ["No key insights available."]),
                "severity": raw_risk.get("severity", 5)  # Default to 5 if missing
            })

    if risks:
        plot_risk_levels(risks)  # Generate visualization safely

    search_results[topic] = {"news": news, "risks": risks}
    return jsonify({"status": "done"})


@app.route("/results/<topic>", methods=["GET"])
def results(topic):  # ✅ Use topic from URL directly
    print("Requested Topic:", topic)  # ✅ Debugging

    if not topic:
        return "⚠️ No topic provided.", 400  # Return error if no topic is provided

    data = search_results.get(topic, {"news": [], "risks": []})

    # ✅ Ensure all risk items have required keys to prevent errors
    risks = []
    for risk in data["risks"]:
        if isinstance(risk, str):  # If risk data is a raw string, attempt to parse
            try:
                risk = json.loads(risk)
            except json.JSONDecodeError:
                risk = {}
        risks.append({
            "project_overview": risk.get("project_overview", "No overview available."),
            "key_factors": risk.get("key_factors", ["No key factors identified."]),
            "key_points": risk.get("key_points", ["No key insights available."]),
            "severity": risk.get("severity", "N/A")
        })

    return render_template("results.html", topic=topic, news=data["news"], risks=risks)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)