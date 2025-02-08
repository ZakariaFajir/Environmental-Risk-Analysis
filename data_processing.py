# data_processing.py

import pandas as pd
import re

def clean_text(text):
    """
    Cleans text by removing special characters, multiple spaces, and non-alphanumeric content.
    """
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def preprocess_news_data(news):
    """
    Prepares the news dataset for AI analysis by cleaning text and structuring data.
    """
    df = pd.DataFrame(news)
    df["cleaned_summary"] = df["summary"].apply(clean_text)
    return df

if __name__ == '__main__':
    sample_news = [
        {"title": "Air Pollution Rising", "summary": "Air quality index worsens in major cities due to emissions!"},
        {"title": "Deforestation Increasing", "summary": "Large-scale tree cutting leads to environmental damage..."}
    ]
    processed_news = preprocess_news_data(sample_news)
    print(processed_news)