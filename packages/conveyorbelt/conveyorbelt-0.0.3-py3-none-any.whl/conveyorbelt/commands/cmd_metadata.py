import logging

import click

LOGGER = logging.getLogger(__name__)


def get_meta(meta: dict, item: str):
    for m in meta:
        if m["name"] == item:
            return m["values"][0]["value"]
    return None


def get_assay(assays: dict, assay: str, item: str):
    for a in assays:
        if a['category'] == assay:
            for m in a['meta']:
                if m["name"] == item:
                    return m["values"][0]["value"]
    return None


@click.command()
@click.option('--run_id', help='Local run identifier (covid19...)', required=True)
@click.option('--output', help='Path to output csv file', required=False)
def command(run_id: str, output: str):
    """
    Execute the query and print the result
    """

    import conveyorbelt.worker
    import conveyorbelt.utils

    result = conveyorbelt.worker.run_task('worker.db.tasks.get_specimens_by_run_identifier', run_identifier=run_id)
    print(",".join(["central_sample_id",
                    "adm1",
                    "received_date",
                    "collection_date",
                    "source_age",
                    "source_sex",
                    "is_surveillance",
                    "is_hcw",
                    "employing_hospital_name",
                    "employing_hospital_trust_or_board",
                    "is_hospital_patient",
                    "admitted_with_covid_diagnosis",
                    "admission_date",
                    "admitted_hospital_name",
                    "admitted_hospital_trust_or_board",
                    "is_care_home_worker",
                    "is_care_home_resident",
                    "anonymised_care_home_code",
                    "adm2",
                    "adm2_private",
                    "biosample_source_id",
                    "root_sample_id",
                    "sender_sample_id",
                    "collecting_org",
                    "sample_type_collected",
                    "sample_type_received",
                    "swab_site",
                    "epi_cluster",
                    "investigation_name",
                    "investigation_site",
                    "investigation_cluster",
                    "ct_1_ct_value",
                    "ct_1_test_target",
                    "ct_1_test_platform",
                    "ct_1_test_kit",
                    "ct_2_ct_value",
                    "ct_2_test_target",
                    "ct_2_test_platform",
                    "ct_2_test_kit",
                    "library_name",
                    "library_seq_kit",
                    "library_seq_protocol",
                    "library_layout_config",
                    "library_selection",
                    "library_source",
                    "library_strategy",
                    "library_layout_insert_length",
                    "library_layout_read_length",
                    "barcode",
                    "artic_primers",
                    "artic_protocol",
                    "run_name",
                    "instrument_make",
                    "instrument_model",
                    "start_time",
                    "end_time",
                    "flowcell_id",
                    "flowcell_type"]))
    for patient in result:
        specimen = patient["specimens"][0]
        m = specimen['meta']
        a = specimen['aliquots'][0]['assays']
        line = list()
        line.append(specimen['external_id'])
        line.append('UK-ENG')
        line.append('')
        line.append(get_meta(m, 'collection_date'))
        line.append(get_meta(patient['meta'], 'age'))
        line.append(get_meta(patient['meta'], 'gender'))
        line.append('Y')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append(get_meta(m, 'county'))
        line.append('')
        line.append(specimen['local_id'])
        line.append('')
        line.append('')
        line.append('SHEF')
        line.append(get_meta(m, 'sample_type'))
        line.append('')
        line.append(get_meta(m, 'sample_site'))
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append('')
        line.append(get_assay(a, 'library', 'library_identifier'))
        line.append(get_assay(a, 'library', 'library_seq_kit'))
        line.append(get_assay(a, 'library', 'library_seq_protocol'))
        line.append(get_assay(a, 'library', 'library_layout_config'))
        line.append(get_assay(a, 'library', 'library_selection'))
        line.append('VIRAL_RNA')
        line.append(get_assay(a, 'library', 'library_strategy'))
        line.append('')
        line.append('')
        line.append(get_assay(a, 'library', 'barcode'))
        line.append(get_assay(a, 'pcr', 'primer_version'))
        line.append(get_assay(a, 'primary_analysis', 'pipline_version'))
        line.append(get_assay(a, 'sequencing', 'nanopore_identifier'))
        line.append(get_assay(a, 'sequencing', 'instrument_make'))

        print(",".join(map(str, line)))
