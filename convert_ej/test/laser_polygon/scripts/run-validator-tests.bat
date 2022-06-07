echo Running 10 validator test(s)
echo Running 10 validator test(s) 1> validator-tests.log
echo Running test #1 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\01 2>> validator-tests.log
if errorlevel 1 (
    echo Validator returned non-zero exit code for a valid test 1>> validator-tests.log
    echo Validator returned non-zero exit code for a valid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #2 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\02 2>> validator-tests.log
if errorlevel 1 (
    echo Validator returned non-zero exit code for a valid test 1>> validator-tests.log
    echo Validator returned non-zero exit code for a valid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #3 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\03 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #4 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\04 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #5 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\05 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #6 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\06 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #7 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\07 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #8 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\08 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #9 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\09 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
echo Running test #10 1>> validator-tests.log
echo Validator comment: 1>> validator-tests.log
files\validator.exe < files\tests\validator-tests\10 2>> validator-tests.log
if not errorlevel 1 (
    echo Validator returned zero exit code for a invalid test 1>> validator-tests.log
    echo Validator returned zero exit code for a invalid test. See validator-tests.log for validator comment
    pause 0
)
del /F /Q validator-tests.log
echo Validator test(s) finished
