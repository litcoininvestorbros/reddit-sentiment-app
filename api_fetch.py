"""
"""
from os import getenv
import time
import praw
import database
import utils


def instanciate_reddit_api_obj():
    """
    """
    # Set up Reddit API credentials
    reddit = praw.Reddit(
        client_id=getenv('R_CLIENT_ID'),
        client_secret=getenv('R_CLIENT_SECRET'),
        user_agent=getenv('R_USER_AGENT')
    )
    return reddit


def fetch_paginated_to_db(subreddit_name: str) -> None:
    """Initial fetch of submissions, using pagination. Saves results
     to database.
    """
    reddit = instanciate_reddit_api_obj()
    subreddit = reddit.subreddit(subreddit_name)

    submissions = []
    last_submission = None
    while True:
        new_submissions = list(subreddit.new(limit=1000, params={'after': last_submission}))
        if not new_submissions:
            break
        submissions.extend(new_submissions)
        last_submission = new_submissions[-1].fullname
        time.sleep(2)  # Sleep to avoid hitting rate limits

    submissions_data_0 = [utils.extract_submission_data(s) for s in submissions]
    submissions_data = [utils.apply_sentiment_score_vader(s) for s in submissions_data_0]

    database.insert_rows_to_table('submissions', submissions_data)


def fetch_stream_to_db(subreddit_name: str) -> None:
    """Fetch of submissions, using pagination. Saves results
     to database.
    """
    reddit = instanciate_reddit_api_obj()

    # Stream post submissions in selected subreddit and analyze sentiment
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.stream.submissions():
        if submission.stickied:  # if post is pinned, skip it
            continue
        submission_data_0 = utils.extract_submission_data(submission)
        submission_data = utils.apply_sentiment_score_vader(submission_data_0)

        database.insert_rows_to_table('submissions', submission_data)
