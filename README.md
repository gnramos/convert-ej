# ejbridge

Tools for translating questions between electronic judges.

## Installation

```
pip install -i https://test.pypi.org/project/EJ-Bridge/
```

## Usage

Creating coderunner problems using a codeforces problems.
```
ejbridge cf2cr files
```
Parameters:

* files : name of the .zip file, or the name of a path with .zip files inside;
* -p : string argument for penalties;
* -an : boolean argument to activate the all-or-nothing parameter;
* -l : string argument to create problems in a specific programming language. ('c', 'cpp' or 'python').