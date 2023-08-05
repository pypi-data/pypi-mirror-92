from irc.bot import SingleServerIRCBot
from irc.client import ServerConnection, Event

from .commands import COMMANDS
from .events import EVENTS
from .models import TwitchTags


class BitBitBot(SingleServerIRCBot):
    SERVER = 'irc.chat.twitch.tv'
    PORT = 6667

    def __init__(self, username: str, token: str, channel: str):
        self.username = username
        self.channel = '#' + channel

        super().__init__(
            server_list=[
                (self.SERVER, self.PORT, token),
            ],
            nickname=self.username,
            realname=self.username,
        )

    def on_welcome(self, conn: ServerConnection, event: Event):
        conn.cap('REQ', ':twitch.tv/membership')
        conn.cap('REQ', ':twitch.tv/tags')
        conn.cap('REQ', ':twitch.tv/commands')
        conn.join(self.channel)
        print('Bot is live')

    def on_pubmsg(self, conn: ServerConnection, event: Event):
        msg = event.arguments[0]
        tags = TwitchTags.parse_obj({
            tag['key'].replace('-', '_'): tag['value']
            for tag in event.tags
        })
        if msg[0] == '!':
            command, *parts = msg[1:].split()
            if command in COMMANDS:
                COMMANDS[command](self, ' '.join(parts), tags)

        self.emit_event(
            'chat_message',
            {
                'msg': msg,
                'tags': TwitchTags,
            }
        )

    def send_message(self, message: str) -> None:
        self.connection.privmsg(self.channel, message)

    def emit_event(self, event_name: str, event_data) -> None:
        for listener in EVENTS[event_name]:
            listener(event_data)
