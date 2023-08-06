import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--date', help='Date in format 2020-11-30', required=True, default="today")
def command(date: str = 'today'):
    """
    Start the hoci community sequences task
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task('worker.reporting.tasks.community_seqs', date=date)
    conveyorbelt.utils.jprint(result)
