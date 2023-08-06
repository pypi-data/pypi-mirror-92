import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
def command():
    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task('worker.dissemination.tasks.phe')
    conveyorbelt.utils.jprint(result)
