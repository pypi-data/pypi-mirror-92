import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
def command():
    """
    Get worker configuration
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task('worker.tasks.get_config')
    conveyorbelt.utils.jprint(result)
