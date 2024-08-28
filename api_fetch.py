"""
"""
import time
import database
import utils



def save_initial_submissions_to_db(subreddit_name: str) -> None:
    """Fetch submissions with pagination and save to database.
    """
    reddit = utils.load_reddit_api_obj()
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

    database.insert_rows('submissions', submissions_data)


def save_streamdata_to_db(subreddit_name: str) -> None:
    """
    """
    reddit = utils.load_reddit_api_obj()

    # Stream post submissions in selected subreddit and analyze sentiment
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.stream.submissions():
        if submission.stickied:  # if post is pinned, skip it
            continue
        submission_data_0 = utils.extract_submission_data(submission)
        submission_data = utils.apply_sentiment_score_vader(submission_data_0)

        database.insert_rows('submissions', submission_data)
