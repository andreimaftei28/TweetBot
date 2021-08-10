import tweepy
import logging
import time
import random
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


from api_creator import create_api
api = create_api()


def fav_retweet(api):
    """
    Like and retweets mentions
    This function will search for tweets that mention your Twitter
    handle and will like and retweet each tweet it finds.
    """

    logger.info('Retrieving tweets...')
    mentions = api.mentions_timeline(tweet_mode='extended')
    for mention in reversed(mentions):
        if mention.in_reply_to_status_id is not None or mention.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return

        if not mention.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                mention.favorite()
                logger.info(f"Liked tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)

        if not mention.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                mention.retweet()
                logger.info(f"Retweeted tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)


def fav_retweet_user(api, user_handle):
    """
    Just like and retweet one user's tweets
    The function fav_retweet_user does the same thing as fav_retweet,
    but rather looks for tweets mentioning another user than youself.
    """


    search_query = f"{user_handle} -filter:retweets"
    logger.info(f'Retrieving tweets mentioning {user_handle}...')
    tweets = api.search(q=search_query, lang ="en")
    for tweet in tweets:
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
                logger.info(f"Liked a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                logger.info(f"Retweeted a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)



def follow_followers(api):
    """
    Follow users who follow your Twitter account
    This is a nice little function that will follow an account that follows your Twitter account.
    If the follow_followers function is used in a loop,
    it will be able to follow anyone back as soon as they start following you.
    It can also be used once-off.
    """

    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            try:
                follower.follow()
                logger.info(f"Following {follower.name}")
            except tweepy.error.TweepError:
                pass


def unfollow(api, follower_id = None):
    """
    The unfollow function can be used to:
    Mass un-follow everyone you currently follow.
    There may not be a lot of scenarios where you want to do that, but you can.
    Unfollow just a certain user. You need to give that user's username,
    user ID or displayed name as an input to the function (follower_id)
    This function on default will unfollow everyone you follow,
    so make sure you use it correctly, or you will have to painfully
    try and remember who you used to follow..
    """

    if not follower_id:
        logger.info("Retrieving current users being followed...")
        for following_id in tweepy.Cursor(api.friends).items():
            try:
                api.destroy_friendship(following_id.id)
                logger.info(f"Unfollowed {following_id.name}")
            except tweepy.error.TweepError:
                pass
    else:
        try:
            api.destroy_friendship(follower_id)
            logger.info(f"Unfollowed {follower_id}...")
        except tweepy.error.TweepError:
            pass


def retweet_tweets_with_hashtag(api, need_hashtags):
    """
    Retweet any tweets with a certain hashtags in the text
    When you are interested in certain topics and want to make sure that you engage with other like-minded users on Twitter, you can use the function
    retweet_tweets_with_hashtag to make sure do you do not miss any tweets.
    """

    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended')
        for tweet in tweets:
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#').lower() for hashtag in need_hashtags]
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id:
                        if not tweet.favorited:
                            # Mark it as Liked, since we have not done it yet
                            try:
                                tweet.favorite()
                                logger.info(f"Liked a tweet mentioning {tweet.user.name}")
                            except Exception as e:
                                logger.error("Error on fav", exc_info=False)
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(5)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=False)
    else:
        logger.error("Hashtag search terms needs to be of type list", exc_info=True)
        return



def tweet_daily(api, text):
    """
    Tweet out a daily tweet
    The function will tweet out a string given to it once every day.
    """
    api.update_status(text)
    logger.info(f"Tweeted {text} at {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}")
    return datetime.now()

# next function is to be editated to match the message that should be posted
# I have created this type of message while in a competition from jetBrains Academy
def create_tweet_message():
    """
    create the message that you want to post
    edit this function accordingly
    """
    dt = datetime.today()
    dau = int(dt.day)
    with open("path/to/file" , "r") as file:
        step = file.read().rstrip()
    project_ids = [68, 69, 73, 74, 78, 79, 80, 82, 85, 90, 92, 94, 96, 97, 98, 99, 102, 105, 109,
                   112, 114, 115, 127, 128, 131, 134, 146, 155, 156, 157, 162, 167, 175, 176]
    remaining = 30 - dau
    if remaining == 0:
        message = f"#Day{dau} - Last day of #JetBrainsAcademy30DayCoding Challenge!\n" \
                  f"Today I solved https://hyperskill.org/learn/step/{step}\n" \
                  f"It has been an amazing journey!!!\n" \
                  f"Thanks #JetBrainsAcademy from @JetBrains_Edu!"
    elif remaining == 15:
        message = f"#Day{dau} of #JetBrainsAcademy30DayCoding Challenge!\n" \
                  f"Yeah...we're halfway there!\n" \
                  f"Today I solved https://hyperskill.org/learn/step/{step}\n" \
                  f"Check out this project if you haven't already:https://hyperskill.org/projects/{project_ids[dau - 1]}\n" \
                  f"Happy Coding with #JetBrainsAcademy from @JetBrains_Edu!"
    elif remaining <= 10:
        message = f"#Day{dau} of #JetBrainsAcademy30DayCoding Challenge!\n" \
                  f"Only {remaining} {'day' if remaining == 1 else 'days'} to go!#dontgiveupnow!\n" \
                  f"Today I solved https://hyperskill.org/learn/step/{step}\n" \
                  f"Check out this project if you haven't already:https://hyperskill.org/projects/{project_ids[dau - 1]}\n" \
                  f"Happy Coding with #JetBrainsAcademy from @JetBrains_Edu!"
    else:
        message = f"#Day{dau} of #JetBrainsAcademy30DayCoding Challenge!\n" \
                  f"Looking forward to the next {remaining} {'day' if remaining == 1 else 'days'}!\n" \
                  f"Today I solved https://hyperskill.org/learn/step/{step}\n" \
                  f"Check out this project if you haven't already:https://hyperskill.org/projects/{project_ids[dau - 1]}\n" \
                  f"Happy Coding with #JetBrainsAcademy from @JetBrains_Edu!"
    
    return message

def main():
    text = create_tweet_message()
    api = create_api()

    fav_retweet_user(api,"@JetBrains_Edu")
    retweet_tweets_with_hashtag(api, ["#JetBrainsAcademy"])

    tweet_daily(api, text)
    logger.info("Waiting...")
    follow_followers(api)


if __name__ == "__main__":
   main()

#m = create_tweet_message()
#print(len(m), m)
#retweet_tweets_with_hashtag(create_api(), ["#JetBrainsAcademy"])