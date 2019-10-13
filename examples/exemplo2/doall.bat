rem   *** validation ***
call scripts\run-validator-tests.bat
call scripts\run-checker-tests.bat

rem    *** tests ***
md tests
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 8" "tests\04" 4
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 9" "tests\05" 5
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 10" "tests\06" 6
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 11" "tests\08" 8
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 123" "tests\09" 9
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 768" "tests\10" 10
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 42" "tests\11" 11
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 6436" "tests\12" 12
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 23424654" "tests\13" 13
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 903" "tests\14" 14
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 2335" "tests\15" 15
call scripts\gen-input-via-stdout.bat "py -3 files\generator.pys3 1285" "tests\16" 16
call scripts\gen-answer.bat tests\01 tests\01.a "tests" ""
call scripts\gen-answer.bat tests\02 tests\02.a "tests" ""
call scripts\gen-answer.bat tests\03 tests\03.a "tests" ""
call scripts\gen-answer.bat tests\04 tests\04.a "tests" ""
call scripts\gen-answer.bat tests\05 tests\05.a "tests" ""
call scripts\gen-answer.bat tests\06 tests\06.a "tests" ""
call scripts\gen-answer.bat tests\07 tests\07.a "tests" ""
call scripts\gen-answer.bat tests\08 tests\08.a "tests" ""
call scripts\gen-answer.bat tests\09 tests\09.a "tests" ""
call scripts\gen-answer.bat tests\10 tests\10.a "tests" ""
call scripts\gen-answer.bat tests\11 tests\11.a "tests" ""
call scripts\gen-answer.bat tests\12 tests\12.a "tests" ""
call scripts\gen-answer.bat tests\13 tests\13.a "tests" ""
call scripts\gen-answer.bat tests\14 tests\14.a "tests" ""
call scripts\gen-answer.bat tests\15 tests\15.a "tests" ""
call scripts\gen-answer.bat tests\16 tests\16.a "tests" ""
call scripts\gen-answer.bat tests\17 tests\17.a "tests" ""
call scripts\gen-answer.bat tests\18 tests\18.a "tests" ""

