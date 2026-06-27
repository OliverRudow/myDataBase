# myDataBase

myDataBase is a basic python package that is providing basic functions to handle either PANDAS of SQLite tables. 
In case of a SQLite application fundamental data base functions are offered. 

# Installation

Install the package easily via `pip`:

pip install mydatabase

## Project Structure

Since this package contains multiple files, here is a quick overview of how the modules interact:

myDataBase/
│
├── __init__.py
├── mySQLDataBase.py                       # SQLite fundamental functions
├── mySQLDataBaseConfiguration.py          # functions to read config files
└── mySQLDataBaseDefinitions.py            # SQLite DataBase definition parameter
├── myTableBase.py                         # common functions
├── myTablePandas.py                       # PANDAS specific functions
├── myTableSQL.py                          # SQLite specific functions
```

## Usage

Provide a simple, complete code example. Show how to import and use the different files.

```python
from your_package import core, utils

# Example using a function from core.py
result = core.main_function("input.txt")

# Example using a helper from utils.py
formatted_data = utils.format_data(result)
print(formatted_data)
```

## Documentation & API
Link to your full documentation here (e.g., Read the Docs) or briefly describe the primary classes and functions of each file.

## Contributing
How can other developers help with the project? Briefly mention how to open issues or submit pull requests.

## License
This project is licensed under the [MIT License](https://opensource.org).