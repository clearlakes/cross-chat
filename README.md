# Cross-chat bot for Discord
This is just an example of a cross-chat bot for anyone who wants to know how it works / host one themselves.

This bot is also one of my first projects in Python, so if anything can be improved be sure to let me know.

Credit goes to the many Stack Overflow questions that have helped me in figuring out what is needed to make it work!

## Commands
The commands included are as follows:
- `.setchannel` = sets the cross-chatting channel to the one that the command is sent in
- `.mod (user)` and `.unmod (user)` = mods and unmods a user (moderators have access to the blacklist commands, only the bot owner can send `.mod` and `.unmod`)
- `.blacklist (user)` and `.unblacklist (user)` = blacklists and unblacklists a user (bans them from cross-chatting)

These commands (and other stuff) are explained in the [bot.py](https://github.com/go-off-i-guess/cross-chat/blob/master/bot.py) file.

## Running the bot
(The three `.json` files in this repo are necessary for the bot to function.)

In the [bot.py](https://github.com/go-off-i-guess/cross-chat/blob/master/bot.py) file, replace [`'YOUR BOTS TOKEN HERE'`](https://github.com/go-off-i-guess/cross-chat/blob/master/bot.py#L6) with the bot token you got from creating your bot [here](https://discord.com/developers/applications).

You can then run the `bot.py` file by sending `python bot.py` in a command prompt window / terminal (you should also install Python (and any missing modules indicated at the beginning of the `bot.py` file) if you haven't already; I used Python 3.8)
