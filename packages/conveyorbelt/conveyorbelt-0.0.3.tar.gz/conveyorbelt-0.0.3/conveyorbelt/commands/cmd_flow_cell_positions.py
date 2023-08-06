import click

import conveyorbelt.utils
import conveyorbelt.worker


@click.command()
def command(**kwargs):
    """
    List sequencer devices
    """

    result = conveyorbelt.worker.run_task('worker.minknow.tasks.flow_cell_positions')
    conveyorbelt.utils.jprint(result)
