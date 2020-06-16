import sys
import json
import argparse
from sqlite3 import OperationalError as sqlite3OperationalError

from playhouse import migrate as mgt
from peewee import OperationalError as peeweeOperationalError

from candig.server.repo import models

dbTypes = {"Text": mgt.TextField, "Integer": mgt.IntegerField}


def addColumns(migrator, newColumnsDict):
    for tableName in newColumnsDict:
        for columnName in newColumnsDict[tableName]:
            columnType = newColumnsDict[tableName][columnName]["type"]
            isNull = newColumnsDict[tableName][columnName]["null"]
            if columnType not in dbTypes:
                print(
                    "Data type {} is not a valid datatype.".format(columnType)
                )
                continue
            try:
                print(
                    'Adding column "{}" to table "{}".'.format(
                        columnName, tableName
                    )
                )
                mgt.migrate(
                    migrator.add_column(
                        tableName, columnName, dbTypes[columnType](null=isNull)
                    )
                )
            except (sqlite3OperationalError, peeweeOperationalError):
                print(
                    'Error adding column "{}" to table "{}"'.format(
                        columnName, tableName
                    )
                )
    print("Done.")


def executeMigration(migrator, newColumnsDict=None, newValuesDict=None):
    if not any([newColumnsDict, newValuesDict]):
        return

    if newColumnsDict:
        addColumns(migrator, newColumnsDict)

    if newValuesDict:
        pass


def readPlayHouseDatabase(dbFile):
    my_db = mgt.SqliteDatabase(dbFile)
    return my_db


def createMigrator(dbFile):
    """
    Create migrator to "dbFile" database file
    """
    my_db = readPlayHouseDatabase(dbFile)
    return mgt.SqliteMigrator(my_db)


def initializePeeWeeDatabase(db_file):
    """
    Initialize PeeWee database
    """
    database = models.SqliteDatabase(db_file, **{})
    models.databaseProxy.initialize(database)


def loadJsonFile(jsonFilePath):
    """
    Load JSON file from 'jsonFilePath' path
    """

    with open(jsonFilePath) as f:
        data = json.load(f)
    return data


def main(args=None):
    """
    Main Routine
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser("Migrate database")
    parser.add_argument(
        "--database", default="registry.db", help="Path to the database file"
    )
    parser.add_argument(
        "--add_columns",
        help="JSON file describing the columns that will be added to the tables",
    )

    args, _ = parser.parse_known_args()

    addColumnsJsonFile = args.add_columns
    dbFile = args.database

    initializePeeWeeDatabase(args)
    migrator = createMigrator(dbFile)

    if addColumnsJsonFile:
        addColumnsJsonFile = loadJsonFile(addColumnsJsonFile)
        executeMigration(migrator, newColumnsDict=addColumnsJsonFile)


if __name__ == "__main__":
    main()
