import os
import argparse
from datetime import datetime

import jinja2
from peewee import SqliteDatabase, DatabaseError
from playhouse.reflection import (
    generate_models,
)
from pandas import DataFrame


"""
Create a CanDIG-Server Database Snapshot Report.

usage: python snapshot_stats.py [-h] [--markdown] [--html]
                       [--destination /output/directory/]
                       database

positional arguments:
  database              Path do CanDIG-Server database file

optional arguments (at ):
  -h, --help            show this help message and exit
  --destination /output/directory/
                        Directory where the outputs will be saved
  (At least one of the below arguments must be used)
  --markdown            Generate report in markdown format
  --html                Generate report in HTML format
  
"""

markdown_template = """
# CanDIG-Server Database Snapshot Report

Report generated on {{current_utc}} UTC.
This report is generated for database located at {{database_location}}

## Datasets

The database contains {{number_of_datasets}} datasets

```
{{dataset_list}}
```

## Records

### Clinical
{{clinical_records}}
### Pipeline
{{pipeline_records}}
### Genomic
{{genomic_records}}

## List of patientsIds

{% for key, value in patient_dict.items() %}
### {{key}} dataset
```
{{value}}
```
{% endfor %}

{% if peer_list %}

## Peers

{{ peer_list }}

{% endif %}

"""

html_template = """
<!DOCTYPE html>
<html>
  <head>
    <title>CanDIG-Server Database Snapshot Report</title>
    <style>
      body {
        font-family: Arial, Helvetica, sans-serif;
      }
    </style>
    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">

    <!-- jQuery library -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>

    <!-- Latest compiled JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> 
  </head>
  <body class="container">
    <h1>CanDIG-Server Database Snapshot Report</h1>

    <p>Report generated on {{current_utc}} UTC.</p>
    <p>This report is generated for database located at <em>{{database_location}}</em></p>    

    <h2>Datasets</h2>

    <p>The database contains {{number_of_datasets}} datasets.</p>

    <code> {{dataset_list}} </code>

    <h2>Records</h2>

    <h3>Clinical</h3>
    {{clinical_records}}
    <h3>Pipeline</h3>
    {{pipeline_records}}
    <h3>Genomic</h3>
    {{genomic_records}}

    <h2>List of patientIds</h2>

    {% for key, value in patient_dict.items() %}
    <h3>{{key}} dataset</h3>
    <code> {{value}} </code>
    {% endfor %} {% if peer_list %}
    <h2>Peers</h2>
    {{ peer_list }} {% endif %}
  </body>
</html>

"""

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


def get_database_abs_path(file):
    return os.path.abspath(file)


def initiate_models(db_path):
    """ Initiate model from the database file """
    db = SqliteDatabase(db_path)

    try:
        models = generate_models(db)
    except (TypeError, DatabaseError):
        print(
            'File "{}" does not seem to be a valid database file.'.format(
                db_path
            )
        )
        print("Aborting snapshot.")
        return

    return models


def count_datasets(models):
    """ Return the number of datasets on the database """
    dataset_model = models["dataset"]
    return dataset_model.select().count()


def gen_html_table(data):
    """ Generate a HTML table from data"""

    df = DataFrame(data=data)
    table_html = df.to_html().replace("class=\"dataframe\"", "class=\"table\"")

    return table_html


def gen_markdown_table(data):
    """ Generate a Markdown table from data"""
    df = DataFrame(data=data)
    table_markdown = df.to_markdown()

    return table_markdown


def get_clinical_table_count(models):
    """ Count the number of records on the tableds defined in clin_tables"""
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
    """ Count the number of records on the tableds defined in pipe_tables"""
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
    """ Count the number of records on the tableds defined in data_file_tables"""
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
    """ Returns dict of patientsId grouped by datasets"""

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
    """ Returns a list of available peers """
    peer_model = models["peer"]
    return [peer.url for peer in peer_model.select()]


def get_jinja_parser(path):
    """ Create the jinja2 parser """
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path))


def generate_rendered_template(jinja_environment, template_filename, **kwargs):
    """Returns rendered template
    args:
    jinja_environment: Jinja2 Parser from get_jinja_parser
    template_filename: Path to template that will be used
    kwargs: Keyword arguments containing the fields on `template_filename` and
        the values to be processed
    """
    return jinja_environment.get_template(template_filename).render(kwargs)


def write_file(file_path, content):
    """ Write `content` on file `file_path` """
    with open(file_path, "w") as result_file:
        result_file.write(content)


def create_argparser():
    """ Creates argpars object """
    parser = argparse.ArgumentParser(
        description="Create a CanDIG-Server Database Snapshot Report"
    )
    parser.add_argument(
        "database",
        metavar="database",
        type=str,
        help="Path to CanDIG-Server database file",
    )

    parser.add_argument(
        "--markdown",
        help="Generate report in markdown format",
        action="store_true",
    )
    parser.add_argument(
        "--html", help="Generate report in HTML format", action="store_true"
    )

    parser.add_argument(
        "--destination",
        help="Directory where the outputs will be saved",
        metavar="/output/directory/",
        default="",
    )

    return parser


def main():
    args = create_argparser().parse_args()

    if not any([args.markdown, args.html]):
        print(
            "Please, specify the output format.\n"
            'Execute "python snapshot_stats.py --help" for a list of available options.'
        )
        return

    destination_path = ""

    if args.destination:
        if os.path.isdir(args.destination):
            destination_path = args.destination
        else:
            print('"{}" is not a valid destination.'.format(args.destination))
            print("Aborting snapshot.")
            return

    models = initiate_models(args.database)

    if models is None:
        return

    database_location = get_database_abs_path(args.database)

    datasets_count = count_datasets(models)

    patient_dict = get_dataset_patients_dict(models)
    peer_list = get_peer_list(models)

    pipeline_records = get_pipeline_table_count(models)
    clinical_records = get_clinical_table_count(models)
    genomic_records = get_genomic_table_count(models)

    # This might be used on the future to
    # save the output on a file
    # environment = get_jinja_parser()

    if args.markdown:
        pipeline_records_md = gen_markdown_table(pipeline_records)
        clinical_records_md = gen_markdown_table(clinical_records)
        genomic_records_md = gen_markdown_table(genomic_records)

        # template_filename = "snapshot_templates/template.md"
        rendered_filename = "output.md"
        # template_file_path = os.path.join(script_path, template_filename)
        rendered_file_path = os.path.join(destination_path, rendered_filename)

        tm = jinja2.Template(markdown_template)
        output_text = tm.render(
            database_location=database_location,
            number_of_datasets=datasets_count,
            clinical_records=clinical_records_md,
            pipeline_records=pipeline_records_md,
            genomic_records=genomic_records_md,
            patient_dict=patient_dict,
            current_utc=datetime.utcnow(),
            dataset_list=[x for x in patient_dict.keys()],
            peer_list=peer_list,
        )

        # output_text = generate_rendered_template(
        #     jinja_environment=environment,
        #     template_filename=template_filename,
        #     number_of_datasets=datasets_count,
        #     clinical_records=clinical_records,
        #     pipeline_records=pipeline_records,
        #     genomic_records=genomic_records,
        #     patient_dict=patient_dict,
        #     current_utc=datetime.utcnow(),
        #     dataset_list=[x for x in patient_dict.keys()],
        #     peer_list=peer_list,
        # )

        write_file(rendered_file_path, output_text)

    if args.html:
        pipeline_records_html = gen_html_table(pipeline_records)
        clinical_records_html = gen_html_table(clinical_records)
        genomic_records_html = gen_html_table(genomic_records)

        # template_filename = "snapshot_templates/template.html"
        rendered_filename = "output.html"
        # template_file_path = os.path.join(script_path, template_filename)
        rendered_file_path = os.path.join(destination_path, rendered_filename)

        tm = jinja2.Template(html_template)
        output_text = tm.render(
            database_location=database_location,
            number_of_datasets=datasets_count,
            clinical_records=clinical_records_html,
            pipeline_records=pipeline_records_html,
            genomic_records=genomic_records_html,
            patient_dict=patient_dict,
            current_utc=datetime.utcnow(),
            dataset_list=[x for x in patient_dict.keys()],
            peer_list=peer_list,
        )

        # output_text = generate_rendered_template(
        #     jinja_environment=environment,
        #     template_filename=template_filename,
        #     number_of_datasets=datasets_count,
        #     clinical_records=clinical_records,
        #     pipeline_records=pipeline_records,
        #     genomic_records=genomic_records,
        #     patient_dict=patient_dict,
        #     current_utc=datetime.utcnow(),
        #     dataset_list=[x for x in patient_dict.keys()],
        #     peer_list=peer_list,
        # )

        write_file(rendered_file_path, output_text)


if __name__ == "__main__":
    main()
