import sys
from datetime import datetime
from peewee import SqliteDatabase
from playhouse.reflection import generate_models, print_model, print_table_sql

current_utc = datetime.utcnow()
print("Report generated on {}".format(current_utc))

# TODO: make this more robust
# Usage: python snapshot_stats.py <path_to_database_file>
db = SqliteDatabase(sys.argv[1])

models = generate_models(db)
globals().update(models) # Upgrade all of the tables to be global variables

# number of total datasets
print("The database contains {} datasets".format(dataset.select().count()))

# TODO: print the number of records under each table for each dataset, maybe in the form of a table
for e in dataset.select():
    print(e.name)
    for table in [patient, sample, diagnosis, sample, treatment, chemotherapy, celltransplant, study, labtest, outcome, slide, consent, immunotherapy, complication, enrollment, tumourboard, surgery, radiotherapy, variantset, readgroupset]:
        print(table)
        print(table.select().where(table.datasetId == e).count())

# TODO: Print out a list of patient IDs for every table

# TODO: Determine the output of this, do we use txt, rst, or something else?
