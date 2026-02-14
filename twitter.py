from common import *
import tweepy
import requests
import io
import time
import random

api11 = tweepy.API(tweepy.OAuth1UserHandler(
    consumer_key=os.getenv("TWITTER_CONSUMER_KEY"), 
    consumer_secret=os.getenv("TWITTER_CONSUMER_SECRET"), 
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"), 
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
))

api2 = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY"), 
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"), 
    access_token = os.getenv("TWITTER_ACCESS_TOKEN"), 
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )

tweets_file = load_json('articles_tweets.json')
EXTENTIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png"
}

def tweet_thread(tweets):
    for tweet in tweets:
        image = tweet["Image"]
        thread = tweet["Tweets"]
        tweet_id = None
        for t in thread:
            time.sleep(random.randint(30, 90))
            if tweet_id is None:
                media_id = upload_image(image) if image else None
                media_ids = [media_id] if media_id else None
                response = api2.create_tweet(text=t, media_ids=media_ids)
            else:
                response = api2.create_tweet(text=t, in_reply_to_tweet_id=tweet_id)
            tweet_id = response.data['id']

def get_image_url(image):
    response = requests.get(image)
    if response.status_code == 200:
        return image
    return None

def upload_image(image_url):
    image_data = requests.get(image_url).content
    file_obj = io.BytesIO(image_data)
    file_type = requests.head(image_url).headers['Content-Type']
    ext = EXTENTIONS[file_type]
    media = api11.media_upload(filename=f'temp{ext}', file=file_obj)
    return media.media_id_string

if __name__ == "__main__":
    tweets_file = tweets_file[3:4]
    # print(tweets_file)
    tweet_thread(tweets_file)
    # print(os.getenv("TWITTER_CONSUMER_KEY") is not None)
    # print(os.getenv("TWITTER_ACCESS_TOKEN") is not None)
    # print(api11.verify_credentials())