from pathlib import Path
from os import mkdir


def install(args):
    plugin_dir = Path('plugins')
    try:
        mkdir(plugin_dir)
    except FileExistsError:
        pass


def plugin_install_parser(plugins_subparsers):
    install_parser = plugins_subparsers.add_parser(
        'install',
        help='Manage your plugins for the bot',
    )

    install_parser.set_defaults(func=lambda __: install_parser.print_help())
