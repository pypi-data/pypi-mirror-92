SUBPARSERS = []


def parser(parser):
    SUBPARSERS.append(parser)
    return parser


def load_subparsers(subparsers):
    for parser in SUBPARSERS:
        parser(subparsers)
