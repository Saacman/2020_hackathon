import tweepy
from config import create_api
import time

def check_mentions(api, since_id):
    print("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue

        if not tweet.user.following:
            tweet.user.follow()
        print(tweet.id)
        api.update_status("Replied", tweet.id)
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        # Check mentions every minute
        time.sleep(60)

if __name__ == "__main__":
    main()
