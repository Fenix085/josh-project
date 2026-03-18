from late import Late as Zernio
from common import *

ZERNIO_API_KEY = os.environ.get("ZERNIO_API_KEY")
client = Zernio(api_key=ZERNIO_API_KEY)

TWITTER_ID = os.environ.get("ZERNIO_TWITTER_ID")
THREADS_ID = os.environ.get("ZERNIO_THREADS_ID")

def post_thread(item):
    image = item.get("Image")
    tweets = item["Tweets"]

    thread_items = []
    for i, tweet in enumerate(tweets):
        entry = {"content": tweet}
        if i == 0 and image:
            entry["mediaItems"] = [{"type": "image", "url": image}]
        thread_items.append(entry)

    platforms = []

    if TWITTER_ID:
        platforms.append({
            "platform": "twitter",
            "accountId": TWITTER_ID,
            "platformSpecificData": {
                "threadItems": thread_items
            }
        })
 
    if THREADS_ID:
        platforms.append({
            "platform": "threads",
            "accountId": THREADS_ID,
            "platformSpecificData": {
                "threadItems": thread_items
            }
        })

    if not platforms:
        print("No platforms")
        return False
    
    try:
        result = client.posts.create(
            content=tweets[0],
            platforms=platforms,
            publish_now=True
        )
        return result
    except Exception as e:
        print(f"Error posting thread: {e}")
        return None
    
if __name__ == "__main__":
    queue = load_from_gist("articles_tweets.json")
    unposted = [item for item in queue if not item.get("posted")]
    if unposted:
        post_thread(unposted[0])
    else:
        print("No unposted items in queue")