"""
"""
from dotenv import dotenv_values
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import praw

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Bug in prod environment requires this to be loaded 
# in the global scope
env = dotenv_values('.env')


def load_reddit_api_obj():
    """
    """
    # Set up Reddit API credentials
    reddit = praw.Reddit(
        client_id=env['R_CLIENT_ID'],
        client_secret=env['R_CLIENT_SECRET'],
        user_agent=env['R_USER_AGENT']
    )
    return reddit


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
