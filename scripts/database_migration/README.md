## Usage

**Note: Make sure the `candig-server` virtual environment is activated before running the script!**

In order to make changes on database, please pass below arguments:
  
`--database` : Path to database file

`--add_columns`: Path to json file describing the changes to be performed on the database.
Please note, json structure must follow this schema:
```python
{
  "table name": {
    "column name": {
      "type": "column type", 
      "null": bool}
  }
}
```

Here's an example:
```json
{
  "Outcome": {
    "siteOfRelapseOrProgression": {
      "type": "Text",
      "null": true
    },
    "siteOfRelapseOrProgressionTier": {
      "type": "Integer",
      "null": true
    }
  },
  "Tumourboard": {
    "actionableExpressionOutlier": {
      "type": "Text",
      "null": true
    },
    "actionableExpressionOutlierTier": {
      "type": "Integer",
      "null": true
    }
  }
}
```

Example:
```bash
 python migration.py --database registry.db --add_columns add_columns.json 
