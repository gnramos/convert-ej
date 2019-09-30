# ejbridge

Tools for translating questions between electronic judges.

## Installation

```
pip install -i https://test.pypi.org/simple/ EJ-Bridge
```

## Usage

The following commands will create a .xml file from a Codeforces question

Creating a file from the name_dir_question directory
```
ejbridge -q name_dir_question
```

Creating files from the folders inside the name_dir directory
```
ejbridge -d name_dir
```
