"""
"""
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon
nltk.download('vader_lexicon')


def load_env_variables() -> dict:
    """
    """
    with open('.env', encoding='utf-8') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value


def extract_submission_data(submission):
    """
    """
    submission_data = {
        'id': submission.id,
        'created_utc': int(submission.created_utc),
        'subreddit': submission.subreddit.display_name,
        'author_name': submission.author.name if submission.author else None,
        'title': submission.title,
        'selftext': submission.selftext,
        'url': submission.url,
        'num_comments': submission.num_comments,
        'score': submission.score,
        'upvote_ratio': submission.upvote_ratio
    }
    return submission_data


def apply_sentiment_score_vader(submission_data: dict) -> dict:
    """
    """
    # Initialize the VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    sentiment_title = sia.polarity_scores(submission_data['title'])
    sentiment_selftext = sia.polarity_scores(submission_data['selftext'])

    sentiment_title_vader = sentiment_title['compound']
    sentiment_selftext_vader = sentiment_selftext['compound'] if submission_data['selftext'] else None

    submission_data['sentiment_title_vader'] = sentiment_title_vader
    submission_data['sentiment_selftext_vader'] = sentiment_selftext_vader

    return submission_data
