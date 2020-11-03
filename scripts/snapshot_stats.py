import sys
from datetime import datetime
from peewee import SqliteDatabase
from playhouse.reflection import generate_models  # print_model, print_table_sql

current_utc = datetime.utcnow()
print("Report generated on {} UTC".format(current_utc))

# TODO: make this more robust
# Usage: python snapshot_stats.py <path_to_database_file>
db = SqliteDatabase(sys.argv[1])

models = generate_models(db)
# globals().update(models)  # Upgrade all of the tables to be global variables

# number of total datasets
dataset_model = models['dataset']
print("The database contains {} datasets".format(dataset_model.select().count()))

dataset_query = dataset_model.select()

clin_tables = ['patient', 'sample', 'diagnosis', 'sample', 'treatment', 'chemotherapy', 'celltransplant', 'study', 'labtest', 'outcome', 'slide', 'consent', 'immunotherapy', 'complication', 'enrollment', 'tumourboard', 'surgery', 'radiotherapy', 'variantset', 'readgroupset']

# TODO: print the number of records under each table for each dataset, maybe in the form of a table
for d in dataset_query:
    print(d.name)
    for table in clin_tables:
        table_model = models[table]
        print(table)
        print(table.select().where(table.datasetId == d).count())

# TODO: Print out a list of patient IDs for every table
patient_model = models['patient']
for d in dataset_query:
    print(d.name)
    print([patient.name for patient in patient_model.select().where(patient_model.datasetId == d)])


# TODO: Determine the output of this, do we use txt, rst, or something else?
