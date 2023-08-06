import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--file', help='xls file containing metadata to import', required=True)
def command(file: str):
    import conveyorbelt.worker
    import conveyorbelt.utils

    LOGGER.info(file)
