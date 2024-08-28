"""
"""
import database
import utils


def save_streamdata_to_db(subreddit_name: str) -> None:
    """
    """
    reddit = utils.load_reddit_api_obj()

    # Stream post submissions in selected subreddit and analyze sentiment
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.stream.submissions():
        if submission.stickied:  # if post is pinned, skip it
            continue
        submission_data = utils.extract_submission_data(submission)
        submission_data = utils.apply_sentiment_score_vader(submission_data)

        database.insert_rows('submissions', submission_data)
