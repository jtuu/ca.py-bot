import os
import json
import re
import urllib.request
import praw
from discord import Embed
from ..utils import rchop

trigger = re.compile("^!r(?:eddit)?")
keywords = ["r", "reddit", "fun"]
base_url = "https://reddit.com"
INIT_UNINIT = 1
INIT_SUCCESS = 2
INIT_FAIL = 3
init_status = INIT_UNINIT
config = None
reddit = None

def init():
    global init_status, config, reddit
    try:
        config_file = open(os.path.abspath(os.path.dirname(__file__) + "/reddit.json"))
    except OSError as err:
        pass
    else:
        try:
            config = json.load(config_file)
        except json.decoder.JSONDecodeError as err:
            pass
        else:
            try:
                reddit = praw.Reddit(
                    client_id=config["client_id"],
                    client_secret=config["client_secret"],
                    user_agent=config["user_agent"],
                    username=config["username"],
                    password=config["password"])
                init_status = INIT_SUCCESS
                return
            except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as err:
                pass
    print("Reddit plugin initialization failed: %s" % (err))
    init_status = INIT_FAIL

def hasattr_oftype(o, p, t):
    return hasattr(o, p) and isinstance(getattr(o, p), t)

def side_effect(arg):
    pass

def fetch_post(post):
    try:
        # this is the recommended way to fetch a lazy object in praw...
        side_effect(post.title)
    except Exception as err:
        print("Could not fetch Reddit post: %s" % (err))
        return None
    else:
        return post

def make_post_url(post):
    return base_url + post.permalink

def embed_reddit_video(post):
    embed = Embed()
    reddit_video = post.secure_media["reddit_video"]
    embed.title = post.title
    embed.url = rchop(reddit_video["fallback_url"], "?source=fallback")
    embed.set_author(name="Reddit", url=make_post_url(post))
    embed.set_thumbnail(url=post.thumbnail)
    return embed

def embed_oembed(post):
    embed = Embed()
    oembed = post.secure_media["oembed"]
    embed.title = post.title
    embed.url = oembed.get("url", post.url)
    if "provider_name" in oembed:
        embed.set_author(name=oembed["provider_name"])
    return embed

def get_post_content(post):
    # some kind of embeddable link post
    if hasattr_oftype(post, "secure_media", dict):
        # reddit video
        if "reddit_video" in post.secure_media:
            return embed_reddit_video(post)
        # oembed
        elif "oembed" in post.secure_media and "url" in post.secure_media["oembed"]:
            return embed_oembed(post)
    # regular link post
    if hasattr(post, "url"):
        return post.url
    return make_post_url(post)


async def action(bot, msg):
    """**!r** _subreddit_
Show random post from a subreddit.
`!r bigfoot`"""
    if init_status == INIT_UNINIT:
        init()
    if init_status == INIT_FAIL:
        return
    args = msg.clean_content.split(" ")[1:]
    sr = reddit.random_subreddit() if len(args) < 1 else reddit.subreddit(args[0])
    post = fetch_post(sr.random())
    if post:
        result = get_post_content(post)
        if isinstance(result, Embed):
            await bot.send_message(msg.channel, embed=result, escape_formatting=False)
        else:
            await bot.send_message(msg.channel, result, escape_formatting=False)
    
