import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
# @click.option('--run_id', help='Local run identifier (covid19...)', required=True)
# @click.option('--protocol_run_id', help='Sequencer job identifier', required=True)
def command():


    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task('worker.dissemination.tasks.phe')
    conveyorbelt.utils.jprint(result)
