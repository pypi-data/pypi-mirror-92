import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier "covid19-2020-..."', required=True)
@click.option('--external_id', help='Sample external id "SHEF-..."', required=True)
@click.option('--local_id', help='Local sample id "NV..."', required=True)

def command(run_id: str, external_id: str, local_id: str):
    """
    Run a single HOCI report
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task(
        'worker.reporting.tasks.start',
        external_id=external_id,
        local_id=local_id,
        run_id=run_id
    )
    conveyorbelt.utils.jprint(result)
