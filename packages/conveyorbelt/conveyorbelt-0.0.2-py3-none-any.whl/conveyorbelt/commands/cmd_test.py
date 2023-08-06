import click


@click.group()
def command():
    pass


@command.command()
def cheese():
    print('cheese')


@command.command()
def cake():
    print('cake')
