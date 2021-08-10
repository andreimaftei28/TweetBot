# TweetBot

## What's included
  * Api creator using Tweepy
## Functions
  * Like and Retweet mentions
  * Like and retweet one user's tweets
  * Follow users who follow your Twitter account
  * Unfollow users on Twitter
  * Retweet any tweet with a certain hashtag
  * Tweet out a daily tweet 

## Requirements and Installation

### Apply for Twitter Developer Account -- follow the steps on [RealPython](https://realpython.com/twitter-bot-python-tweepy/)

**Clone The Repository**

```
  * Make sure you have python installed
python --version

  * Clone the app
git clone https://github.com/andreimaftei28/TweetBot.git

  * Switch to directory
cd TweetBot

  * Create virtual env(make sure you have virtualenv installed)
virtualenv --python=python3 venv

  * Activate virtual env
source venv/bin/activate

  * Install Package dependencies
pip install -r requirements.txt

  * Add your Twitter app credentials in the secrets.py
(Tune some other options if you like)

# Start the application

- Run the app - **python twitter_bot.py **
or
- Add this call to your crontab(unix)/task scheduler(windows) (or something similar) to retweet/ like all new tweets regularly
```

## Technologies

- [Python](https://www.python.org/) Python is powerful... and fast; plays well with others; runs everywhere; is friendly & easy to learn; is Open.
  
- [Tweepy](https://pypi.org/project/tweepy/) - Tweepy: Twitter for Python!
