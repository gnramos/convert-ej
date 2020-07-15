# convert-ej

A software tool for converting problem files between electronic judges formats.

[TestPypi link](https://pypi.org/project/convert-ej/).

## Installation

```
pip install convert-ej
```

## Usage

```
convert-ej reader writer file
```

The tool _reads_ a problem in _file_, structured in a specific format, and then _writes_ it into a different format. The user needs to provide the following command line arguments:
* **reader**: the input format (e.g. _Polygon_).
* **writer**: the output format (e.g. _BOCA_).
* **file**: the path to the file (or directory) containing the problem in the _reader_ format.

### Example

To convert a problem in **Polygon** format into a **CodeRunner** one, we can use:

```
convert-ej Polygon CodeRunner polygon_problem.zip
```

More details can be found using _help_ function:
```
convert-ej --help
```
