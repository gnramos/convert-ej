# ejbridge

Tools for translating questions between electronic judges.

[TestPypi link](https://test.pypi.org/project/EJ-Bridge/).

## Installation

```
pip install -i https://test.pypi.org/simple/ EJ-Bridge
```

## Usage

## Codeforces to Coderunner

Creating coderunner problems using a codeforces problems.
```
ejbridge cf2cr files
```
Parameters:

* files : name of the .zip file, or the name of a path with .zip files inside;
* -p : string argument for penalties;
* -an : boolean argument to activate the all-or-nothing parameter;
* -l : string argument to create problems in a specific programming language. ('c', 'cpp' or 'python').

## Codeforces to BOCA
	
Creating a BOCA contest using codeforces problems.

```
ejbridge cf2boca files
```

Parameters:

* files : name of the .zip files used to build the contest, in order.