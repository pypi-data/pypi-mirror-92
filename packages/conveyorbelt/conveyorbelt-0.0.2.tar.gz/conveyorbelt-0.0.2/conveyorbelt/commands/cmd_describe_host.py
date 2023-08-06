import click

import conveyorbelt.utils
import conveyorbelt.worker


@click.command()
def command(**kwargs):
    """
    Get sequencer info
    """

    result = conveyorbelt.worker.run_task('worker.minknow.tasks.describe_host')
    conveyorbelt.utils.jprint(result)
