from argparse import ArgumentParser
from pkgutil import iter_modules
from pathlib import Path
from pkgutil import walk_packages
from os import mkdir

from bitbitbot import parsers


def discover_plugins():
    plugins_path = Path('plugins')
    try:
        mkdir(plugins_path)
    except FileExistsError:
        pass

    for child in plugins_path.iterdir():
        if child.is_dir():
            mod_infos = walk_packages(
                [child.absolute()],
                '.'.join(child.parts) + '.'
            )
            for __, name, __ in mod_infos:
                __import__(name, fromlist=['_trash'])


def main():
    parser = ArgumentParser(
        prog='bitbitbot',
        description='A command line interface for the BitBitBot Twitch Chat Bot',
    )
    parser.set_defaults(func=lambda __: parser.print_help())
    subparsers = parser.add_subparsers(help='commands')

    for __, name, __ in iter_modules(parsers.__path__, f'{parsers.__name__}.'):
        __import__(name, fromlist=['_trash'])

    parsers.load_subparsers(subparsers)
    discover_plugins()

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
