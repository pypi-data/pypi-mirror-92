# BitBitBot
An unopinionated, extensible Python ChatBot built for twitch on top of the [irc library](https://pypi.org/project/irc/). For more information, please refer to the documentation.

## Example Usage
```python
from bitbitbot.bot

bot = BitBitBot(
    {bot_account_name},         # bitbitbot
    {bot_oauth_token},          # oauth:123456890asdfgh
    {streamer_channel_name},    # metabytez
)

bot.start()
```

## Creating Plugins
Assuming you have installed bitbitbot in a virtualenv called `.venv` and then create the following project structure
```
|- my_bot
|- - .venv
|- - plugins
|- - - my_plugin
|- - - - commands.py
```
You can add the following code to the `commands.py` file, to register your first command.
```python
from bitbitbot import command
from bitbitbot.bot import BitBitBot
from bitbitbot.models import TwitchTags


@command('foo')
def foo(bot: BitBitBot, msg: str, tags: TwitchTags) -> None:
    bot.send_message('Hello World!')
```

The name of the directories inside of `plugins` can be whatever you want, but the root directory must be called `plugins`

You can have multiple directories in the `plugins` directory

You can add multiple commands to a single `commands.py` file.

The name of the function does not have to match the command name.

You don't need the type annotations, they are just for demonstration purposes.
