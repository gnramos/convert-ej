# Convert-EJ

Tools for converting different electronic judges question formats.

[TestPypi link](https://pypi.org/project/Convert-EJ/).

## Installation

```
pip install Convert-EJ
```

## Usage
The file can be translated by using the command line tool "convert-ej":
```
convert-ej reader writer file_name
```

Parameters:

* **reader**: input format (Implemented: BOCA, Polygon);
* **writer**: output format (Implemented: BOCA, CodeRunner);
* **name**: name of the file or directory with the questions to be translated;

More informations can be found in the help function:
```
convert-ej -h
```

## Example

To convert a **Polygon** question named file.zip into a **CodeRunner** one, we can use:

```
convert-ej Polygon CodeRunner file.zip
```

The specific parameters for the formats used can be found using the help function:

```
convert-ej Polygon CodeRunner file.zip -h
```