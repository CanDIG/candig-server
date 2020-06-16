## Usage

In order to make changes on database, please pass below arguments:
  
`--database` : Path to database file 
`--add_columns`: Path to json file describing the changes to the dabase

Example:
```bash
 python migration.py --database registry.db --add_columns add_columns.json 
