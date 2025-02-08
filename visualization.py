import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib

matplotlib.use("Agg")

# ✅ Ensure Matplotlib supports emojis
matplotlib.rcParams["font.family"] = "Arial Unicode MS"  # Windows/Mac

def plot_risk_levels(risks):
    """Creates a bar chart of environmental risks based on severity."""
    if not risks:
        print("⚠️ No risk data available.")
        return

    df = pd.DataFrame(risks)

    # ✅ Ensure proper column names before plotting
    if "risk" not in df.columns or "severity" not in df.columns:
        print(f"⚠️ Missing required columns 'risk' or 'severity' in data.\nData received: {df}")
        return

    # Explode list values so that each key factor gets its own row
    df = df.explode("risk")

    plt.figure(figsize=(12, 6))
    sns.barplot(x="risk", y="severity", data=df, palette="coolwarm")
    plt.xticks(rotation=45)
    plt.xlabel("Risk Factors")
    plt.ylabel("Severity Level")
    plt.title("Environmental Risk Analysis")
    plt.tight_layout()

    plt.savefig("static/risk_chart.png")
    print("✅ Risk chart saved successfully!")


def plot_trend_over_time(trend_data):
    """
    Generates a line chart showing the trend of an environmental risk over time.
    """
    df = pd.DataFrame(trend_data)
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='date', y='impact', data=df, marker='o')
    plt.xlabel("Date")
    plt.ylabel("Impact Level")
    plt.title("Environmental Risk Trend Over Time")
    plt.grid()
    plt.show()

if __name__ == '__main__':
    sample_risk_data = [
        {"risk": "Air Pollution", "severity": 8},
        {"risk": "Deforestation", "severity": 7},
        {"risk": "Climate Change", "severity": 9},
        {"risk": "Water Scarcity", "severity": 6}
    ]
    plot_risk_levels(sample_risk_data)
    
    sample_trend_data = [
        {"date": "2024-01", "impact": 5},
        {"date": "2024-02", "impact": 6},
        {"date": "2024-03", "impact": 8},
        {"date": "2024-04", "impact": 9}
    ]
    plot_trend_over_time(sample_trend_data)