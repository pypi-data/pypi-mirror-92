import logging

import click

LOGGER = logging.getLogger(__name__)


@click.command()
@click.option('--run_id', help='Local run identifier "covid19-2020-..."', required=True)
def command(run_id: str):
    """
    Prepare HPC job configuration files and run the primary analysis job on the HPC.
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    conveyorbelt.worker.run_task('worker.sequencing.tasks.prepare_hpc_job', run_id=run_id)

    result = conveyorbelt.worker.run_task('worker.sequencing.tasks.run_hpc_analysis_job', run_id=run_id)
    conveyorbelt.utils.jprint(result)
