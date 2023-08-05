from bitbitbot.parsers import parser

from ._install import plugin_install_parser


@parser
def plugins_parser(subparsers):
    plugin_parser = subparsers.add_parser(
        'plugins',
        help='Manage your plugins for the bot',
    )

    plugins_subparsers = plugin_parser.add_subparsers(help='subcommands')
    plugin_install_parser(plugins_subparsers)

    plugin_parser.set_defaults(func=lambda __: plugin_parser.print_help())
