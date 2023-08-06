import json

import click.utils


def jprint(obj, **kwargs):
    """
    Print JSON-serialised objects to the standard output.
    """
    click.utils.echo(message=json.dumps(obj, indent=2), **kwargs)


def build_run_info(run_id: str, protocol_run_id: str) -> dict:
    """
    Make the metadata for worker requests

    @param run_id: COG-UK Sheffield run identifier e.g. 'covid19-20200827-141436'
    @param protocol_run_id: Sequencer protocol run identifier e.g. '652941d0-2ed9-4aa9-bfb2-e31aa45df869'
    @return:
    """
    return dict(
        run_id=run_id,
        protocol_run=dict(
            run_id=protocol_run_id,
            user_info=dict(
                protocol_group_id=run_id,
                sample_id=run_id,
            )
        )
    )
