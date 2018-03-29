import re
import mwclient
import itertools
import time

trigger = re.compile("^!hitler")
keywords = ["hitler", "wiki", "wikipedia", "game"]

match_pattern = re.compile(r"^!hitler\s*(\d*)")

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

            selected = next(itertools.islice(links, idx, idx + 1))
            self.history.append(selected)
            self.current = selected
            self.current_links = None
        
game = None
idle_timeout = 120
last_activity = 0

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
    del game

async def action(bot, msg):
    """**!hitler** [_num_]
Play the Wikipedia Hitler game. The point is to start from a random page and get to the Hitler page in as few links as possible."""
    match = match_pattern.match(msg.clean_content)
    if match:
        game = get_game()
        game.get_next_action()(match.groups()[0])
        output = game.get_history() + "\n"
        if game.won():
            output += "You're winner! Score: %d" % game.get_score()
            delete_game()
        else:
            output += game.get_link_list(formatted=True)
        await bot.send_message(msg.channel, output, escape_formatting=False)
