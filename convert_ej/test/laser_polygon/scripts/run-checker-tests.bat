echo Running 6 checker test(s)
echo Running 6 checker test(s) 1> checker-tests.log
echo Running test #1 1>> checker-tests.log
echo Checker comment: 1>> checker-tests.log
check.exe files\tests\checker-tests\01 files\tests\checker-tests\01.o files\tests\checker-tests\01.a 2>> checker-tests.log
if not %ERRORLEVEL% EQU 0 (
    echo Checker returned incorrect verdict. Expected: OK 1>> checker-tests.log
    echo Checker returned incorrect verdict. Expected: OK. See checker-tests.log for checker comment
    pause 0
)
echo Running test #2 1>> checker-tests.log
echo Checker comment: 1>> checker-tests.log
check.exe files\tests\checker-tests\02 files\tests\checker-tests\02.o files\tests\checker-tests\02.a 2>> checker-tests.log
if not %ERRORLEVEL% EQU 0 (
    echo Checker returned incorrect verdict. Expected: OK 1>> checker-tests.log
    echo Checker returned incorrect verdict. Expected: OK. See checker-tests.log for checker comment
    pause 0
)
echo Running test #3 1>> checker-tests.log
echo Checker comment: 1>> checker-tests.log
check.exe files\tests\checker-tests\03 files\tests\checker-tests\03.o files\tests\checker-tests\03.a 2>> checker-tests.log
if not %ERRORLEVEL% EQU 0 (
    echo Checker returned incorrect verdict. Expected: OK 1>> checker-tests.log
    echo Checker returned incorrect verdict. Expected: OK. See checker-tests.log for checker comment
    pause 0
)
echo Running test #4 1>> checker-tests.log
echo Checker comment: 1>> checker-tests.log
check.exe files\tests\checker-tests\04 files\tests\checker-tests\04.o files\tests\checker-tests\04.a 2>> checker-tests.log
if not %ERRORLEVEL% EQU 0 (
    echo Checker returned incorrect verdict. Expected: OK 1>> checker-tests.log
    echo Checker returned incorrect verdict. Expected: OK. See checker-tests.log for checker comment
    pause 0
)
echo Running test #5 1>> checker-tests.log
echo Checker comment: 1>> checker-tests.log
check.exe files\tests\checker-tests\05 files\tests\checker-tests\05.o files\tests\checker-tests\05.a 2>> checker-tests.log
if not %ERRORLEVEL% EQU 1 (
    echo Checker returned incorrect verdict. Expected: Wrong answer 1>> checker-tests.log
    echo Checker returned incorrect verdict. Expected: Wrong answer. See checker-tests.log for checker comment
    pause 0
)
echo Running test #6 1>> checker-tests.log
echo Checker comment: 1>> checker-tests.log
check.exe files\tests\checker-tests\06 files\tests\checker-tests\06.o files\tests\checker-tests\06.a 2>> checker-tests.log
if not %ERRORLEVEL% EQU 1 (
    echo Checker returned incorrect verdict. Expected: Wrong answer 1>> checker-tests.log
    echo Checker returned incorrect verdict. Expected: Wrong answer. See checker-tests.log for checker comment
    pause 0
)
del /F /Q checker-tests.log
echo Checker test(s) finished
