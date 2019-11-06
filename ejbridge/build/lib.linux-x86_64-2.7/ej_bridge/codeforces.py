import os
import shutil
import xml.etree.ElementTree as ET


def create_paths(question_name):
    i_f = 'intermadiate_files'
    i_q = i_f + '/' + question_name
    i_s = i_q + '/solutions'
    if not os.path.exists(i_f):
        os.mkdir(i_f)

    if os.path.exists(i_q):
        shutil.rmtree(i_q)

    os.mkdir(i_q)
    os.mkdir(i_s)


def codeforces_to_intermediate(directory, question_name):
    create_paths(question_name)

    i_q = 'intermadiate_files/' + question_name
    dir_text = directory + '/statement-sections/english'
    dir_tests = directory + '/tests'

    shutil.copytree(dir_text, i_q + '/text')
    shutil.copytree(dir_tests, i_q + '/testcases')

    shutil.copy(directory + '/tags', i_q)

    solutiontype = ''
    name_dir = os.listdir(directory+'/solutions')
    for name in name_dir:
        if name.endswith('.c'):
            namesolution = name
            solutiontype = "c_program"
            break
    else:
        for name in name_dir:
            if name.endswith('.desc'):
                with open(directory+'/solutions/'+name) as desc:
                    if 'Tag: MAIN' in desc.read():
                        namesolution = name[:-5]
                        if namesolution.endswith('.py'):
                            solutiontype = 'python3'
                        elif namesolution.endswith('.cpp'):
                            solutiontype = 'cpp_program'
    with open(i_q + '/type', 'w') as sol_file:
        sol_file.write(solutiontype)

    dir_sol = directory + '/solutions/' + namesolution
    shutil.copy(dir_sol, i_q + '/solutions')

    treeproblem = ET.parse(directory + '/problem.xml')
    rootproblem = treeproblem.getroot()

    for data in rootproblem.iter("time-limit"):
        with open(i_q + '/time', 'w') as time_file:
            time_file.write(str(int(int(data.text)/1000)))

    for data in rootproblem.iter("memory-limit"):
        with open(i_q + '/memory', 'w') as memory_file:
            memory_file.write(str(int(int(data.text)/(1024*1024))))
