from crewai.tools import BaseTool
import tweepy
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class TwitterPostTool(BaseTool):
    name: str = "TwitterPostTool"
    description: str = "Posts a tweet to Twitter. Input should be the text of the tweet."
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    bearer_token: Optional[str] = None
    access_token: Optional[str] = None
    access_secret: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = kwargs.get("api_key") or os.getenv("TWITTER_API_KEY")
        self.api_secret = kwargs.get("api_secret") or os.getenv("TWITTER_API_SECRET")
        self.bearer_token = kwargs.get("bearer_token") or os.getenv("TWITTER_BEARER_TOKEN")
        self.access_token = kwargs.get("access_token") or os.getenv("TWITTER_ACCESS_TOKEN")
        self.access_secret = kwargs.get("access_secret") or os.getenv("TWITTER_ACCESS_SECRET")

    def _run(self, text: str) -> str:
        try:
            client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_secret,
            )
            response = client.create_tweet(text=text)
            tweet_id = response.data['id']
            result_message = f"Tweet posted successfully! Tweet ID: {tweet_id}"
            print(f"Twitter API Response: {response}") # Always print the response
            return result_message
        except Exception as e:
            error_message = f"Error posting tweet: {e}"
            print(f"Twitter API Error: {error_message}") # Always print errors
            return error_message

if __name__ == '__main__':
    tool = TwitterPostTool(
        api_key=os.getenv("TWITTER_API_KEY"),
        api_secret=os.getenv("TWITTER_API_SECRET"),
        bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_secret=os.getenv("TWITTER_ACCESS_SECRET"),
    )
    result = tool.run(text="Testing the Twitter posting tool from direct run!")
    print(result)
