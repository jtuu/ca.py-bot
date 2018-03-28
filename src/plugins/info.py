import re
import urllib.request
import os
import json

trigger = re.compile("^!capybot")
keywords = ["capybot", "info", "bot"]

config = json.load(open(os.path.abspath(os.path.dirname(__file__) + "/info.json")))
base_url = "https://api.github.com"

def get_latest_commit_message():
    try:
        branch_response = urllib.request.urlopen(base_url + "/repos/" + config["github"] + "/git/refs/heads/master").read()
        branch_data = json.loads(branch_response.decode("utf-8"))
        commit_response = urllib.request.urlopen(branch_data["object"]["url"]).read()
        commit_data = json.loads(commit_response.decode("utf-8"))
        return commit_data["message"]
    except (urllib.error.HTTPError, json.JSONDecodeError) as err:
        print("Failed to get latest commit message from Github: %s" % err)

async def action(bot, msg):
    """**!capybot**
Displays basic information about this bot."""
    text = "%s made by %s: https://github.com/%s" % (config["name"], config["author"], config["github"]) 
    commit_msg = get_latest_commit_message()
    if commit_msg:
        text += "\nLatest change: " + commit_msg
    await bot.send_message(msg.channel, text)
