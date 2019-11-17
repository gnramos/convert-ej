import os
import shutil
import xml.etree.ElementTree as ET


def create_paths(question_name):
    i_f = 'intermadiate_files'
    inter_quest = os.path.join(i_f, question_name)
    i_s = os.path.join(inter_quest, 'solutions')
    if not os.path.exists(i_f):
        os.mkdir(i_f)

    if os.path.exists(inter_quest):
        shutil.rmtree(inter_quest)

    os.mkdir(inter_quest)
    os.mkdir(i_s)


def get_paths(directory, question_name):
    inter_quest = os.path.join('intermadiate_files', question_name)
    dir_text = os.path.join(directory, 'statement-sections/english')
    dir_tests = os.path.join(directory, 'tests')

    return [inter_quest, dir_text, dir_tests]


def copy_files(dir_sol, dir_text, dir_tests, inter_quest, directory):
    shutil.copy(dir_sol, os.path.join(inter_quest, 'solutions'))

    shutil.copytree(dir_text, os.path.join(inter_quest, 'text'))
    shutil.copytree(dir_tests, os.path.join(inter_quest, 'testcases'))
    shutil.copy(os.path.join(directory, 'tags'), inter_quest)


def get_solution(language, dir_name, directory):
    lan_type = {
        'c': 'c_program',
        'py': 'python3',
        'cpp': 'cpp_program'
    }
    close = False

    if language:
        for name in dir_name:
            if name.endswith('.' + language):
                namesolution = name
                solutiontype = lan_type[language]
                break
        else:
            close = True
    else:
        for name in dir_name:
            if name.endswith('.c'):
                namesolution = name
                solutiontype = 'c_program'
                break
        else:
            for name in dir_name:
                if name.endswith('.desc'):
                    with open(os.path.join(directory, 'solutions', name)) \
                            as desc:
                        if 'Tag: MAIN' in desc.read():
                            namesolution = name[:-5]
                            if namesolution.endswith('.py'):
                                solutiontype = 'python3'
                            elif namesolution.endswith('.cpp'):
                                solutiontype = 'cpp_program'

    return [solutiontype, namesolution, close]


def get_time_and_memory_limits(directory, inter_quest):
    treeproblem = ET.parse(os.path.join(directory, 'problem.xml'))
    rootproblem = treeproblem.getroot()

    for data in rootproblem.iter("time-limit"):
        with open(os.path.join(inter_quest, 'time'), 'w') as time_file:
            time_file.write(str(int(int(data.text)/1000)))

    for data in rootproblem.iter("memory-limit"):
        with open(os.path.join(inter_quest, 'memory'), 'w') as memory_file:
            memory_file.write(str(int(int(data.text)/(1024*1024))))


def codeforces_to_intermediate(directory, question_name, language):

    create_paths(question_name)

    [inter_quest, dir_text, dir_tests] = get_paths(directory, question_name)

    dir_name = os.listdir(os.path.join(directory, 'solutions'))

    [solutiontype, namesolution, close] = get_solution(language,
                                                       dir_name, directory)
    if close:
        return 0

    with open(os.path.join(inter_quest, 'type'), 'w') as sol_file:
        sol_file.write(solutiontype)

    dir_sol = os.path.join(directory, 'solutions', namesolution)

    copy_files(dir_sol, dir_text, dir_tests, inter_quest, directory)

    get_time_and_memory_limits(directory, inter_quest)

    return 1
