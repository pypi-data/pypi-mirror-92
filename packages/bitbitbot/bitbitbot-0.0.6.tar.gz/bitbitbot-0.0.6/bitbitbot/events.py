from collections import defaultdict

EVENTS = defaultdict(list)


def listen(event_name: str) -> callable:
    def _listener(func: callable) -> None:
        EVENTS[event_name].append(func)
    return _listener
