import xml.etree.ElementTree as ET
import os
import zipfile
import shutil
from .t2h import tex2html


# Conjunto de funções para inserir a secção CDATA no xml
def CDATA(text=None):
    element = ET.Element('![CDATA[')
    element.text = text
    return element


ET._original_serialize_xml = ET._serialize_xml


def _serialize_xml(write, elem, qnames, namespaces,
                   short_empty_elements, **kwargs):
    if elem.tag == '![CDATA[':
        write("\n<{}{}]]>\n".format(elem.tag, elem.text))
    else:
        return ET._original_serialize_xml(
            write, elem, qnames, namespaces, short_empty_elements, **kwargs)


ET._serialize_xml = ET._serialize['xml'] = _serialize_xml


def name_section(sec_name, description):
    return '\n<p>\n<b>' + sec_name + description + '\n</p>\n'


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
    # Insere o nome
    with open(dir_sec+'name.tex', 'r') as name:
        root.find("name").find("text").text = name.read()

    sections = {
        'legend': '</b>\n',
        'input': 'Entrada</b><br />\n',
        'output': 'Saida</b><br />\n',
        'notes': 'Notas</b><br />\n'
    }
    # Formata os textos
    for file_name, sec_name in sections.items():
        if os.path.isfile(dir_sec + file_name + '.tex'):
            texto += get_section(dir_sec + file_name + '.tex', sec_name)

    # Insere o texto
    root.find("questiontext").find("text").append(CDATA(texto))

    # Insere tutorial
    if os.path.isfile(dir_sec + 'tutorial.tex'):
        with open(dir_sec + 'tutorial.tex', 'r') as t:
            root.find("generalfeedback").find("text").text = tex2html(t.read())

    solutiontype = ''
    # Insere a solução na questão
    name_dir = os.listdir(directory+'/solutions/')
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

    # Insere a linguagem de programação utilizada
    root.find("coderunnertype").text = solutiontype

    with open(directory+'/solutions/' + namesolution, 'r') as solution:
        root.find("answer").append(CDATA(solution.read()))

    # Faz uma busca por todos os arquivos de teste e os ordena
    tests = os.listdir(directory+'/tests/')
    tests.sort()

    # Encontra os casos testes a serem visualizados pelo aluno
    list_tests_show = []
    tests_show = os.listdir(dir_sec)
    for arq in tests_show:
        if arq.endswith('.a'):
            list_tests_show.append(arq[8:])

    # Insere as entradas e saídas de teste no template
    # e adiciona-o na questão
    for arq in tests:
        if arq.endswith('.a'):
            with open(directory+'/tests/'+arq, 'r') as testout:
                testoroot.find("expected").find("text").text = testout.read()

                if arq in list_tests_show:
                    testoroot.set("useasexample", "1")

                root.find("testcases").append(testoroot)

                testtree = ET.parse(package_dir + 'Testcase-Template.xml')
                testoroot = testtree.getroot()
        else:
            with open(directory+'/tests/'+arq, 'r') as testinput:
                testoroot.find("stdin").find("text").text = testinput.read()

    # Insere as tags
    with open(directory+"/tags", 'r') as tagfile:
        tagscontent = tagfile.readlines()
    taglist = [x.strip() for x in tagscontent]

    tags = root.find("tags")
    for tagelement in taglist:
        tag = ET.Element('tag')
        ET.SubElement(tag, 'text').text = tagelement
        tags.append(tag)

    # Insere tempo e mémoria limite
    treeproblem = ET.parse(directory + '/problem.xml')
    rootproblem = treeproblem.getroot()
    for data in rootproblem.iter("time-limit"):
        root.find("cputimelimitsecs").text = str(int(int(data.text)/1000))
    for data in rootproblem.iter("memory-limit"):
        root.find("memlimitmb").text = str(int(int(data.text)/(1024*1024)))

    # Gera o arquivo final da questão
    files = 'Files'
    if not os.path.exists(files):
        os.mkdir(files)
    tree.write(files + '/' + question_name + '.xml', 'UTF-8')


def dir_cf_to_cr(directory):
    questions = os.listdir(directory)
    for name in questions:
        if name.endswith('.zip'):
            with zipfile.ZipFile(directory + '/' + name, 'r') as zip_ref:
                zip_ref.extractall('tmp')
            xml_gen('tmp', name[:-4])
            shutil.rmtree('tmp')
