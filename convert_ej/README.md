# Source Code

Usage is simple, a [reader](readers.py) gets the problem information from a specific file format and stores it as a generic [problem](problem.py) data structure which can then be used to [write](writers.py) it into a specific file format using the provided [templates](templates) (if necessary). [convert.py](convert.py) contains parsers for interfacing via command line.

## Writers

### BOCA

BOCA's writer creates a PDF file using TeX system (such as [TeX Live](https://www.tug.org/texlive/)) using the `pdflatex` tool. If wish to provide a front page for this PDF, `pdfunite` must also be available in your system. If you plan to convert a [Polygon](https://polygon.codeforces.com/) problem into BOCA and use its [testlib](https://github.com/MikeMirzayanov/testlib) checkers, you'll also need the `g++` compiler.
