import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier "covid19-2020-..."', required=True)
def command(run_id: str):
    """
    Transfer data from the sequencer to the HPC
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    protocol_run = conveyorbelt.worker.run_task('worker.sequencing.tasks.get_protocol_run_info', run_id=run_id)
    conveyorbelt.utils.jprint(protocol_run)
    result = conveyorbelt.worker.run_task('worker.minknow.tasks.transfer_data', run_id=run_id, protocol_run=protocol_run)
    conveyorbelt.utils.jprint(result)
    result = conveyorbelt.worker.run_task('worker.sequencing.tasks.move_finished', run_id=run_id, protocol_run=protocol_run)
    conveyorbelt.utils.jprint(result)
