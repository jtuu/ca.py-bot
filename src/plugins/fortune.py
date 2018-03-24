import re
import subprocess

trigger = re.compile("^!fortune")

fortune_dir = None
fortune_files = []
default_file = "fortunes"
match_pattern = re.compile(r"^!fortune\s+(\S+)")
newline = re.compile(r"\n")
dir_pattern = re.compile(r"^.+?(\/.+)")
file_pattern = re.compile(r"(\S+)$")

async def action(bot, msg):
    global fortune_dir
    if not fortune_dir:
        file_list = newline.split(subprocess.run(["fortune", "-f"], stderr=subprocess.PIPE).stderr.decode("utf-8"))
        dir_match = dir_pattern.match(file_list.pop(0))
        if dir_match:
            fortune_dir = dir_match.groups()[0]
            for line in file_list:
                file_match = file_pattern.search(line)
                if file_match:
                    fortune_files.append(file_match.groups()[0])

    fortune_file = default_file

    option_match = match_pattern.match(msg.clean_content)
    if option_match:
        option = option_match.groups()[0]
        if option in fortune_files:
            fortune_file = option

    fortune = subprocess.run(["fortune", "-s", fortune_dir + "/" + fortune_file], stdout=subprocess.PIPE).stdout.decode("utf-8")
    await bot.send_message(msg.channel, fortune)