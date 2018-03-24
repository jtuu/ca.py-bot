import os
import json
import re
import urllib.request
import xml.etree.cElementTree as etree
from ..utils import querify

trigger = re.compile("^!(?:wolfram|wa)")

match_pattern = re.compile(r"^!(?:wolfram|wa)\s+(.+)")
base_url = "http://api.wolframalpha.com/v2/query"
default_params = json.load(open(os.path.abspath(os.path.dirname(__file__) + "/wolfram.json")))
default_params["format"] = "plaintext"
default_params["parsetimeout"] = 30
default_params["podtimeout"] = 30
default_params["scantimeout"] = 30

result_queries = [
    ".pod[@title='Result']/subpod/plaintext",
    ".pod[@title='Name']/subpod/plaintext",
    ".pod[@title='Basic Information']/subpod/plaintext",
    ".pod[@title='Weather forecast']/subpod/plaintext",
    ".pod[last()]/subpod/plaintext"
]

def format_response(response):
    root = etree.fromstring(response)
    for query in result_queries:
        for element in root.findall(query):
            return element.text

async def action(bot, msg):
    match = match_pattern.match(msg.clean_content)
    if match:
        params = dict(default_params)
        params["input"] = match.groups()[0]
        try:
            response = urllib.request.urlopen(base_url + querify(params)).read()
        except urllib.error.HTTPError as err:
            print("Wolfram Alpha query request failed: %s" % err)
        else:
            formatted = format_response(response)
            if formatted:
                await bot.send_message(msg.channel, formatted)
            else:
                await bot.send_message(msg.channel, "¯\\_(ツ)_/¯")
