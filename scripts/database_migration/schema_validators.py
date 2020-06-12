from jsonschema import validate
from pprint import pprint

add_columns_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "patternProperties": {
        "^.*$": {
            "type": "object",
            "patternProperties": {
                "^.*$": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "null": {"type": "boolean"},
                    },
                    "required": ["type", "null"],
                }
            },
        }
    },
}


def validate_add_columns(columnsDict):
    try:
        validate(
            instance={"name": "Eggs", "price": 34.99},
            schema=add_columns_schema,
        )
    except:
        print("JSON does not follow schema:")
        pprint(
            {
                "table name": {
                    "column name": {"type": "column type", "null": bool}
                }
            }
        )
