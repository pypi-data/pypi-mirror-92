import logging

import json
import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--id', help='Check flow cell free barcodes', required=True)
def command(id: str):
    """
    Update the assay status base on a metadata key and its value, option to update child assays too
    """

    import conveyorbelt.worker
    import conveyorbelt.utils


    result = conveyorbelt.worker.run_task(
        'worker.db.tasks.check_flowcell',
        id=id,

    )
    conveyorbelt.utils.jprint(result)
