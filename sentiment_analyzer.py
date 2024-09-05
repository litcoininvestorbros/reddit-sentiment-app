"""
"""
from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
    tokenizer="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
    max_length=512,
    truncation=True
)

