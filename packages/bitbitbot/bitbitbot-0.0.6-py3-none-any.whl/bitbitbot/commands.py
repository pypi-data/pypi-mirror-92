COMMANDS: dict[str, callable] = {}


def command(command_name: str) -> callable:
    def _func_wrapper(func: callable):
        COMMANDS[command_name] = func
    return _func_wrapper
