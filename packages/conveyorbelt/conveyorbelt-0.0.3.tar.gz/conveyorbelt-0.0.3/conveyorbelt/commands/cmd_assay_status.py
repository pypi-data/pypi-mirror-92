import logging

import json
import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--category',
              help='The assay category; extraction, pcr, library, sequencing, primary_analysis, disemination, reporting',
              required=True)
@click.option('--metadata_key',
              help='The metadata key used to identify which assay you want to change the status of, i.e. run_identifier',
              required=True)
@click.option('--metadata_value', help='The value of the metadata key, i.e. covid19-2020-...', required=True)
@click.option('--status', help='The new assay status; pass, fail, stop, deprecated, pending', required=True)
@click.option('--children', help='Flag for True. This will change the status of all the assays children too',
              required=True, default="False")
def command(category: str, metadata_key: str, metadata_value: str, status: str, children: str):
    """
    Update the assay status base on a metadata key and its value, option to update child assays too
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    print(json.loads(children.lower()))
    result = conveyorbelt.worker.run_task(
        'worker.db.tasks.bulk_set_assay_status',
        category=category,
        metadata_key=metadata_key,
        metadata_value=metadata_value,
        new_status=status,
        children=json.loads(children.lower())
    )
    conveyorbelt.utils.jprint(result)
