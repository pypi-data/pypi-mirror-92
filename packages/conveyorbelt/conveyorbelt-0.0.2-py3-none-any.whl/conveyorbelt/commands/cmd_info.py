import logging

import click

import conveyorbelt.utils
import conveyorbelt.worker

LOGGER = logging.getLogger(__name__)


@click.command()
def command(**kwargs):
    """
    Get user info
    """

    result = conveyorbelt.worker.call('token/info')
    conveyorbelt.utils.jprint(result)
