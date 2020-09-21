# convert-ej

A software tool for converting problem files between electronic judges formats.

[**Pypi link**](https://pypi.org/project/convert-ej/)

## Installation

```
pip3 install convert-ej
```

## Usage

```
convert-ej reader writer file
```

The tool _reads_ a problem in _file_, structured in a specific format, and then _writes_ it into a different format. The user needs to provide the following command line arguments:
* **reader**: the input e-judge format.
* **writer**: the output e-judge format.
* **file**: the path to the file (or directory) containing the problem information, which must be structured according to the _reader_ format.

Please be mindful of the specificities of each e-judge format, since convertion might not be sucessful. For example, CodeRunner does not handle EPS images and BOCA may have issues creating the test sheet (usually a PDF file) dependng on the format the examples.

### Example

To convert a problem in **Polygon** format into a **CodeRunner** one, we can use:

```
convert-ej Polygon CodeRunner polygon_problem.zip
```

More details can be found using _help_ function:
```
convert-ej --help
```
