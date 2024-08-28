"""
"""
import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import database
import utils

# Download the VADER lexicon
nltk.download('vader_lexicon')


def save_streamdata_to_db(subreddit_name: str) -> None:
    """
    """
    # Load environment variables
    env = utils.load_env_variables()

    # Set up Reddit API credentials
    reddit = praw.Reddit(
        client_id=env['R_CLIENT_ID'],
        client_secret=env['R_CLIENT_SECRET'],
        user_agent=env['R_USER_AGENT']
    )

    sia = SentimentIntensityAnalyzer()

    # Stream post submissions in selected subreddit and analyze sentiment
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.stream.submissions():
        if submission.stickied:  # if post is pinned, skip it
            continue

        sentiment_title = sia.polarity_scores(submission.title)
        sentiment_title_vader = sentiment_title['compound']
        sentiment_selftext = sia.polarity_scores(submission.selftext)
        sentiment_selftext_vader = sentiment_selftext['compound'] if submission.selftext else None

        submission_data: list[dict] = [{
            'id': submission.id,
            'created_utc': int(submission.created_utc),
            'subreddit': submission.subreddit.display_name,
            'author_name': submission.author.name,
            'title': submission.title,
            'selftext': submission.selftext,
            'url': submission.url,
            'num_comments': submission.num_comments,
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio,
            'sentiment_title_vader': sentiment_title_vader,
            'sentiment_selftext_vader': sentiment_selftext_vader
        }]

        database.insert_rows('submissions', submission_data)
