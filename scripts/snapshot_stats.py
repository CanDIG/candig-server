import os
import argparse
from datetime import datetime

import jinja2
from peewee import SqliteDatabase
from playhouse.reflection import (
    generate_models,
)
from pandas import DataFrame


# TODO: Docstring

pipe_tables = [
    "extraction",
    "sequencing",
    "alignment",
    "variantcalling",
    "fusiondetection",
    "expressionanalysis",
]

data_file_tables = ["variantset", "readgroupset", "rnaquantificationset"]


clin_tables = [
    "patient",
    "sample",
    "diagnosis",
    "sample",
    "treatment",
    "chemotherapy",
    "celltransplant",
    "study",
    "labtest",
    "outcome",
    "slide",
    "consent",
    "immunotherapy",
    "complication",
    "enrollment",
    "tumourboard",
    "surgery",
    "radiotherapy",
]

script_path = os.path.dirname(os.path.abspath(__file__))


def initiate_models(db_path):
    # TODO Docstring
    db = SqliteDatabase(db_path)

    try:
        models = generate_models(db)
    except TypeError:
        # TODO: Message here
        return

    return models


def count_datasets(models):
    # TODO Docstring
    dataset_model = models["dataset"]
    return dataset_model.select().count()


def gen_html_table(data):
    # TODO docstring

    df = DataFrame(data=data)
    table_html = df.to_html()

    return table_html


def gen_markdown_table(data):
    # TODO docstring
    df = DataFrame(data=data)
    table_markdown = df.to_markdown()

    return table_markdown


def get_clinical_table_count(models):
    # TODO Docstring
    dataset_model = models["dataset"]
    dataset_query = dataset_model.select()

    table_output = {}

    for d in dataset_query:
        ds_dict = table_output.setdefault(d.name, {})

        for table in clin_tables:
            table_model = models[table]
            ds_dict[table] = (
                table_model.select().where(table_model.datasetId == d).count()
            )

    return table_output


def get_pipeline_table_count(models):
    # TODO Docstring
    dataset_model = models["dataset"]
    dataset_query = dataset_model.select()

    table_output = {}

    for d in dataset_query:
        ds_dict = table_output.setdefault(d.name, {})

        for table in pipe_tables:
            table_model = models[table]
            ds_dict[table] = (
                table_model.select().where(table_model.datasetId == d).count()
            )

    return table_output


def get_genomic_table_count(models):
    # TODO Docstring
    dataset_model = models["dataset"]
    dataset_query = dataset_model.select()

    table_output = {}

    for d in dataset_query:
        ds_dict = table_output.setdefault(d.name, {})

        for table in data_file_tables:
            table_model = models[table]
            ds_dict[table] = (
                table_model.select().where(table_model.datasetId == d).count()
            )

    return table_output


def get_dataset_patients_dict(models):
    # TODO Docstring

    dataset_model = models["dataset"]
    dataset_query = dataset_model.select()
    patient_model = models["patient"]
    patient_dict = {}
    for d in dataset_query:
        patient_dict[d.name] = [
            patient.name
            for patient in patient_model.select().where(
                patient_model.datasetId == d
            )
        ]

    return patient_dict


def get_peer_list(models):
    # TODO docstring
    peer_model = models["peer"]
    return [peer.url for peer in peer_model.select()]


def get_jinja_parser():
    # TODO docstring
    return jinja2.Environment(loader=jinja2.FileSystemLoader(script_path))


def generate_rendered_template(jinja_environment, template_filename, **kwargs):
    # TODO docstring
    return jinja_environment.get_template(template_filename).render(kwargs)


def write_file(file_path, content):
    # TODO docstring
    with open(file_path, "w") as result_file:
        result_file.write(content)


def main():
    # TODO docstring

    parser = argparse.ArgumentParser(
        "Create a CanDIG-Server DataBase Snapshot Report"
    )
    parser.add_argument(
        "database",
        metavar="database",
        type=str,
        help="Path do CanDIG-Server database file",
    )

    parser.add_argument(
        "--markdown",
        help="Generate report in markdown format",
        action="store_true",
    )
    parser.add_argument(
        "--html", help="Generate report in HTML format", action="store_true"
    )

    args = parser.parse_args()

    models = initiate_models(args.database)

    if models is None:
        # TODO message
        return

    datasets_count = count_datasets(models)

    patient_dict = get_dataset_patients_dict(models)
    peer_list = get_peer_list(models)

    environment = get_jinja_parser()

    if args.markdown:
        pipeline_records = gen_markdown_table(get_pipeline_table_count(models))
        clinical_records = gen_markdown_table(get_clinical_table_count(models))
        genomic_records = gen_markdown_table(get_genomic_table_count(models))

        template_filename = "snapshot_templates/template.md"
        rendered_filename = "snapshot_outputs/output.md"
        template_file_path = os.path.join(script_path, template_filename)
        rendered_file_path = os.path.join(script_path, rendered_filename)

        output_text = generate_rendered_template(
            jinja_environment=environment,
            template_filename=template_filename,
            number_of_datasets=datasets_count,
            clinical_records=clinical_records,
            pipeline_records=pipeline_records,
            genomic_records=genomic_records,
            patient_dict=patient_dict,
            current_utc=datetime.utcnow(),
            dataset_list=[x for x in patient_dict.keys()],
            peer_list=peer_list,
        )

        write_file(rendered_file_path, output_text)

    if args.html:
        pipeline_records = gen_html_table(get_pipeline_table_count(models))
        clinical_records = gen_html_table(get_clinical_table_count(models))
        genomic_records = gen_html_table(get_genomic_table_count(models))

        template_filename = "snapshot_templates/template.html"
        rendered_filename = "snapshot_outputs/output.html"
        template_file_path = os.path.join(script_path, template_filename)
        rendered_file_path = os.path.join(script_path, rendered_filename)

        output_text = generate_rendered_template(
            jinja_environment=environment,
            template_filename=template_filename,
            number_of_datasets=datasets_count,
            clinical_records=clinical_records,
            pipeline_records=pipeline_records,
            genomic_records=genomic_records,
            patient_dict=patient_dict,
            current_utc=datetime.utcnow(),
            dataset_list=[x for x in patient_dict.keys()],
            peer_list=peer_list,
        )

        write_file(rendered_file_path, output_text)


if __name__ == "__main__":
    main()
