# ejbridge

Tools for translating questions between electronic judges.

[TestPypi link](https://test.pypi.org/project/EJ-Bridge/).

## Installation

```
pip install -i https://test.pypi.org/simple/ EJ-Bridge
```

## Usage
The file can be translated by using the command line tool "ejbridge":
```
ejbridge reader writer file_name
```

Parameters:

* reader : input format (Implemented: BOCA, Polygon);
* writer : output format (Implemented: BOCA, CodeRunner);
* name : name of the file or directory with the questions to be translated;

More informations can be found in the help function:
```
ejbridge -h
```