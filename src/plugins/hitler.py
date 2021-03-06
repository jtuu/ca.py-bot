import re
import mwclient
import itertools
import time
import asyncio

trigger = re.compile("^!hitler")
keywords = ["hitler", "wiki", "wikipedia", "game"]

match_pattern = re.compile(r"^!hitler\s*(\d*)")
newline = re.compile(r"\n")

class HitlerGame():
    def __init__(self):
        self.wiki = mwclient.Site(("https", "en.wikipedia.org"))
        self.goal = 2731583 # Adolf Hitler
        self.current = None
        self.current_links = None
        self.history = []

    def start(self, arg):
        self.current = self.get_random_page()
        self.history.append(self.current)

    def get_next_action(self):
        return self.start if len(self.history) == 0 else self.select_link

    def get_random_page(self):
        return self.wiki.pages[next(self.wiki.random(0, limit=1))["id"]]

    def get_link_list(self, formatted=False):
        links = self.current_links or [link for link in self.current.links(namespace=0) if link.exists]
        self.current_links = links
        if formatted:
            return "\n".join(("%d - %s" % (i, link.name) for i, link in enumerate(links)))
        else:
            return links

    def get_history(self):
        text = "Start"
        for page in self.history[:-1]:
            text += "→" + page.name
        text += "→__" + self.history[-1].name + "__"
        return text

    def won(self):
        return self.current.pageid == self.goal

    def get_score(self):
        return max(0, 10 - len(self.history))

    def select_link(self, arg):
        try:
            idx = int(arg)
        except Exception:
            pass
        else:
            links = self.get_link_list()
            if idx < 0 or idx >= len(links):
                print("selected index out of range", idx, len(links))
                return

            selected = next(itertools.islice(links, idx, idx + 1)) # follow redirects somehow
            self.history.append(selected)
            self.current = selected
            self.current_links = None
        
game = None
idle_timeout = 300
last_activity = 0
last_messages = []

def get_game():
    global game
    global last_activity
    now = time.time()
    if not game or now - last_activity > idle_timeout:
        game = HitlerGame()
    last_activity = now
    return game

def delete_game():
    global game
    game = None

async def action(bot, msg):
    """**!hitler** [_num_]
Play the Wikipedia Hitler game. The point is to start from a random page and get to the Hitler page in as few links as possible."""
    match = match_pattern.match(msg.clean_content)
    if match:
        if len(last_messages):
            coros = []
            first_last = last_messages.pop(0)
            coros.append(bot.edit_message(first_last, newline.split(first_last.content)[0]))
            while len(last_messages):
                last_msg = last_messages.pop()
                coros.append(bot.delete_message(last_msg))
            await asyncio.wait(coros)
        game = get_game()
        game.get_next_action()(match.groups()[0])
        output = game.get_history()
        if game.won():
            output += " **You're winner! Score: %d" % game.get_score() + "**"
            delete_game()
        else:
            output += "\n" + game.get_link_list(formatted=True)
        new_msgs = await bot.send_message(msg.channel, output, escape_formatting=False, split_long=True)
        last_messages.extend(new_msgs)
