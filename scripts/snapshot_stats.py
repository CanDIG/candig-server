import sys
import argparse
from datetime import datetime
from peewee import SqliteDatabase
from playhouse.reflection import generate_models  # print_model, print_table_sql
from pandas import DataFrame

import os
import jinja2


# TODO: Docstring

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
    "variantset",
    "readgroupset",
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


def gen_markdown_table(models):
    table_output = get_tables_count(models)

    df = DataFrame(data=table_output)
    table_markdown = df.to_markdown()

    return table_markdown


def get_tables_count(models):
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


def get_dataset_patients_dict(models):
    # TODO Docstring

    dataset_model = models["dataset"]
    dataset_query = dataset_model.select()
    patient_model = models["patient"]
    patient_dict = {}
    for d in dataset_query:
        patient_dict[d.name] = [
            patient.name
            for patient in patient_model.select().where(patient_model.datasetId == d)
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

    parser = argparse.ArgumentParser("Create a CanDIG-Server DataBase Snapshot Report")
    parser.add_argument(
        "database",
        metavar="database",
        type=str,
        help="Path do CanDIG-Server database file",
    )
    # TODO: Add options like --markdown --json --html --txt?

    args = parser.parse_args()

    models = initiate_models(args.database)

    if models is None:
        # TODO message
        return

    datasets_count = count_datasets(models)
    table_markdown = gen_markdown_table(models)
    patient_dict = get_dataset_patients_dict(models)
    peer_list = get_peer_list(models)

    template_filename = "template.md"
    rendered_filename = "output.md"
    template_file_path = os.path.join(script_path, template_filename)
    rendered_file_path = os.path.join(script_path, rendered_filename)

    environment = get_jinja_parser()

    output_text = generate_rendered_template(
        jinja_environment=environment,
        template_filename=template_filename,
        number_of_datasets=datasets_count,
        records=table_markdown,
        patient_dict=patient_dict,
        current_utc=datetime.utcnow(),
        peer_list=peer_list,
    )

    write_file(rendered_file_path, output_text)


if __name__ == "__main__":
    main()
