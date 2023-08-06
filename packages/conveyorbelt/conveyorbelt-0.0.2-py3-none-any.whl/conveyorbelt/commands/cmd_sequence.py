import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier (covid19...)', required=True)
@click.option('--library_id', help='Library identifier', required=True)
@click.option('--device', help='Sequencer device name', required=True)
@click.option('--flow_cell_id', help='Flow cell identifier on the sequencer', required=True)
def command(run_id: str, library_id: str, device: str, flow_cell_id: str):
    """
    Run the sequencing pipeline
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task('worker.sequencing.tasks.start', run_id=run_id, library_id=library_id, device=device,
                                          flow_cell_id=flow_cell_id)
    conveyorbelt.utils.jprint(result)
