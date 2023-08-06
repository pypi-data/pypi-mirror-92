from typing import List

from twitterbot.TwitterBot import TwitterBot

import arrow
import structlog

from .config import (
    NYCASP_TWITTER_ACCOUNT,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET,
)

logger = structlog.get_logger()

TWEETS_API_URL = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
SUSPENDED_TODAY_TEXT = "#NYCASP rules will be suspended tomorrow, {tomorrow}"


def is_suspended_tomorrow() -> bool:
    tweets = get_nyc_alt_side_parking_tweets()
    tomorrow = arrow.utcnow().shift(days=1).to("US/Eastern")
    return any(
        t.startswith(
            SUSPENDED_TODAY_TEXT.format(
                tomorrow=tomorrow.format("dddd, MMMM D")
            )
        )
        for t in tweets
    )


def get_nyc_alt_side_parking_tweets(count: int = 5) -> List[str]:
    response, tweets = TwitterBot(
        TWITTER_CONSUMER_KEY,
        TWITTER_CONSUMER_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET,
    ).get_tweets(screen_name=NYCASP_TWITTER_ACCOUNT, count=count)
    if response.status != 200:
        logger.error(
            "could not fetch tweets", status=response.status, response=response
        )
        tweets = []
    else:
        tweets = [t["text"] for t in tweets]
    return tweets
