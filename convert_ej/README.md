# Source Code

Usage is simple, a [reader](readers.py) gets the problem information from a specific file format and stores it as a generic [problem](problem.py) data structure which can then be used to [write](writers.py) it into a specific file format using the provided [templates](templates) (if necessary). [convert.py](convert.py) contains parsers for interfacing via command line.
