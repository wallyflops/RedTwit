import praw
import tweepy
from pyshorteners import Shortener
from secrets import *


def get_post(sub, limit=50, user_agent="User-Agent: windows/ubuntu:com.RedTwitApp:v0.1 (by /u/wallyflops)"):
    r = praw.Reddit(user_agent=user_agent)
    submission = r.get_subreddit(sub).get_hot(limit=limit)

    saved_posts = dict()

    for i in submission:
        post_list = list()
        post_list.append(i.title)
        post_list.append(i.url)

        #saved_posts[i.id] = post_list
        yield post_list


    #return saved_posts


def twitter_auth(consumer_token, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def post_twit(post):
    api = twitter_auth(consumer_token, consumer_secret, access_token, access_token_secret)

    url = post[1]
    title = post[0]

    shrt_url = shorten_url(url)
    txt_len = len("{} Source:{}".format(title, shrt_url))
    if txt_len + len(shrt_url) > 140:
        print("STATUS TO SUBMIT: " + title[:118] + ".." + "more {}".format(shrt_url))
        api.update_status(title[3:110] + ".." + "more {}".format(url))
        return True
    else:
        api.update_status(title[3:] + ".." + "more {}".format(url))
        return True


def shorten_url(url):
    # Goo.gl Shortener
    api_key = "AIzaSyBRICfYzs7Q-5ojvnXks2dq213z_fPXqSQ"

    shortener = Shortener('Google', api_key=api_key)
    return shortener.short(url)


def shorten_post(long_post):
    if long_post[0].startswith("TIL"):
        a = long_post[0].replace("TIL", "")
        print(a)


psts = get_post("TodayILearned", limit=5)
for pst in psts:
    shorten_post(pst)
    #try:
    #    post_twit(pst)#
    #except tweepy.error.TweepError:
    #    print("DUPLICATE POST")
    #    continue

    #print("Posted... ENDING")
    #break




