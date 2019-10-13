import xml.etree.ElementTree as ET
import os
from .t2h import tex2html


def name_section(sec_name, description):
    return '\n<p>\n  <b>' + sec_name + '</b><br />\n' + description + '\n</p>\n'


def get_section(file_name, sec_name):
    with open(file_name, 'r') as section:
        text = name_section(sec_name, tex2html(section.read()))
    return text


def xml_gen(directory, question_name):
    # Templates para a questão e para casos teste
    package_dir = os.path.abspath(os.path.dirname(__file__)) + '/'
    tree = ET.parse(package_dir + 'Template.xml')
    root = tree.getroot()
    root = root[0]
    testtree = ET.parse(package_dir + 'Testcase-Template.xml')
    testoroot = testtree.getroot()

    texto = ''  # Texto da questão
    dir_sec = directory + '/statement-sections/english/'  # Diretório do texto

    sections = {
        'legend': '',
        'input': 'Entrada',
        'output': 'Saida',
        'notes': 'Notas'
    }

    for file_name, sec_name in sections:
        if os.path.isfile(dir_sec + file_name + '.xml'):
            texto += get_section(dir_sec + file_name + '.xml', sec_name)

    # Insere o texto
    xmlquestion = root.find("questiontext")
    xmltextquestion = xmlquestion.find("text")
    xmltextquestion.text = texto

    # Insere a solução na questão
    name_dir = os.listdir(directory+'/solutions/')
    for name in name_dir:
        if name.endswith('.cpp') or name.endswith('.c'):
            namesolution = name

    with open(directory+'/solutions/' + namesolution, 'r') as solution:
        xmlsolution = root.find("answer")
        xmlsolution.text = solution.read()

    # Faz uma busca por todos os arquivos de teste e os ordena
    tests = os.listdir(directory+'/tests/')
    tests.sort()

    # Insere as entradas e saídas de teste no template
    # e adiciona-o na questão
    for arq in tests:
        if arq.endswith('.a'):
            with open(directory+'/tests/'+arq, 'r') as testoutput:
                xmloutput = testoroot.find("expected").find("text")
                xmloutput.text = testoutput.read()

                xmltestcases = root.find("testcases")
                xmltestcases.append(testoroot)

                testtree = ET.parse(package_dir + 'Testcase-Template.xml')
                testoroot = testtree.getroot()
        else:
            with open(directory+'/tests/'+arq, 'r') as testinput:
                xmlinput = testoroot.find("stdin").find("text")
                xmlinput.text = testinput.read()

    # Gera o arquivo final da questão
    files = 'files'
    if not os.path.exists(files):
        os.mkdir(files)
    tree.write(files + '/' + question_name + '.xml')


def dir_xml_gen(directory):
    questions = os.listdir(directory)
    for name in questions:
        xml_gen(directory + '/' + name, name)