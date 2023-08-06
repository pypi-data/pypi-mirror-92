import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier (covid19...)', required=True)
@click.option('--protocol_run_id', help='Sequencer job identifier', required=True)
def command(run_id: str, protocol_run_id: str):
    """
    Submit the HPC job
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    run = conveyorbelt.utils.build_run_info(run_id=run_id, protocol_run_id=protocol_run_id)

    result = conveyorbelt.worker.run_task('worker.workflow.tasks.run_job', **run)
    conveyorbelt.utils.jprint(result)
