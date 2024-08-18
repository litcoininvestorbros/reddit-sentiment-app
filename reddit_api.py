"""
"""
from dotenv import dotenv_values
import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import database


# Download the VADER lexicon
nltk.download('vader_lexicon')

def run_data_collection(subreddit_name) -> None:
    """
    """
    # Load environment variables
    env = dotenv_values('./.env')

    # Set up Reddit API credentials
    reddit = praw.Reddit(
        client_id=env['R_CLIENT_ID'],
        client_secret=env['R_CLIENT_SECRET'],
        user_agent=env['R_USER_AGENT']
    )

    sia = SentimentIntensityAnalyzer()

    # Stream post submissions in selected subreddit and analyze sentiment
    subreddit = reddit.subreddit(subreddit_name)
    submission_data = {}  # submission data storage
    for submission in subreddit.stream.submissions():
        if submission.stickied:  # if post is pinned, skip it
            continue
        if not submission.selftext:  # if post doesn't contain text, skip it
            continue

        sentiment = sia.polarity_scores(submission.selftext)

        submission_data[f"{submission.id}"] = {\
            'id': submission.id,
            'created_utc': int(submission.created_utc),
            'num_comments': submission.num_comments,
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio,
            'sentiment': sentiment['compound']
        }
        database.insert_row('sentiment', submission_data)
