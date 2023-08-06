import logging
import pathlib

import click

CMD_SUBDIR = 'commands'
CMD_DIR = pathlib.Path(__file__).parent.joinpath(CMD_SUBDIR)
CMD_PREFIX = 'cmd_'
CMD_FUNC = 'command'


class CLI(click.MultiCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.insert(0, click.core.Option(('--verbose',), help='Debug mode with more logging', is_flag=True,
                                                default=False))
        self.params.insert(0, click.core.Option(('--poll_interval',),
                                                help='How many seconds between each task info retrieval', default=10.,
                                                type=float))

    def list_commands(self, ctx):
        """
        Obtain a list of all available commands.

        :param ctx: Click context
        :return: List of sorted commands
        """
        commands = list()

        # Load commands
        for path in CMD_DIR.glob(CMD_PREFIX + '*.py'):
            start, end = len(CMD_PREFIX), -len(path.suffix)
            commands.append(path.name[start:end])

        commands.sort()

        return commands

    def get_command(self, ctx, name: str):
        """
        Get a specific command by looking up the module.

        :param ctx: Click context
        :param name: Command name
        :return: Module's cli function
        """
        ns = dict()

        filename = CMD_PREFIX + name + '.py'
        path = CMD_DIR.joinpath(filename)

        with open(path) as f:
            code = compile(f.read(), path, 'exec')
        eval(code, ns, ns)

        return ns[CMD_FUNC]


@click.command(cls=CLI)
def main(*args, verbose: bool = False, **kwargs):
    """ Commands to help manage your project. """
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)


if __name__ == '__main__':
    main()
