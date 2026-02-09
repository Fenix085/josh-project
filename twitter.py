from common import *
import tweepy

api = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY"), 
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"), 
    access_token = os.getenv("TWITTER_ACCESS_TOKEN"), 
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )

tweets_file = load_json('articles_tweets.json')

def tweet_thread(tweets):
    for tweet in tweets:
        image = tweet["Image"]
        thread = tweet["Tweets"]
        tweet_id = None
        for t in thread:
            if tweet_id is None:
                response = api.create_tweet(text=t)
            else:
                response = api.create_tweet(text=t, in_reply_to_tweet_id=tweet_id)
            tweet_id = response.data['id']

if __name__ == "__main__":
    tweets_file = tweets_file[:1]
    # print(tweets_file)
    tweet_thread(tweets_file)