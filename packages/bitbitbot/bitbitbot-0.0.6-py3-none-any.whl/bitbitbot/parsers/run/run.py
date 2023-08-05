from os import getenv

from bitbitbot.bot import BitBitBot
from bitbitbot.parsers import parser


def run(args):
    if args.name is None:
        print('ERROR: Missing required argument NAME')
        exit(1)
    if args.token is None:
        print('ERROR: Missing required argument TOKEN')
        exit(1)
    if args.channel is None:
        print('ERROR: Missing required argument CHANNEL')
        exit(1)

    bot = BitBitBot(
        username=args.name,
        token=args.token,
        channel=args.channel,
    )
    bot.start()


@parser
def run_parser(subparsers):
    run_parser = subparsers.add_parser(
        'run',
        help='Run the chat bot',
    )

    run_parser.add_argument(
        '-n', '--name',
        default=getenv('BITBIT_NAME'),
        dest='name',
        help='The name of the account to use for the bot. Defaults to the BITBIT_NAME environment variable',
    )
    run_parser.add_argument(
        '-t', '--token',
        default=getenv('BITBIT_TOKEN'),
        dest='token',
        help='The oauth token for the bot. Defaults to the BITBIT_TOKEN environment variable',
    )
    run_parser.add_argument(
        '-c', '--channel',
        default=getenv('BITBIT_CHANNEL'),
        dest='channel',
        help='The twitch channel the bot should join. Defaults to the BITBIT_CHANNEL environment variable',
    )
    run_parser.set_defaults(func=run)
