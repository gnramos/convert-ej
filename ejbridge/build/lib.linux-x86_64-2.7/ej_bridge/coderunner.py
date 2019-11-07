import xml.etree.ElementTree as ET
import os
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
    return sec_name + description + '\n</p>\n'


def get_section(file_name, sec_name):
    with open(file_name, 'r') as section:
        text = name_section(sec_name, tex2html(section.read()))
    return text


def intermediate_to_coderunner(directory, question_name):
    # Templates para a questão e para casos teste
    package_dir = os.path.abspath(os.path.dirname(__file__)) + '/'
    tree = ET.parse(package_dir + 'Template.xml')
    root = tree.getroot()
    root = root[0]
    testtree = ET.parse(package_dir + 'Testcase-Template.xml')
    testoroot = testtree.getroot()

    texto = ''  # Texto da questão
    dir_sec = directory + '/text/'  # Diretório do texto
    # Insere o nome
    with open(dir_sec+'name.tex', 'r') as name:
        root.find("name").find("text").text = name.read()

    sections = {
        'legend': '<p>',
        'input': '\n<p>\n<b>Entrada</b><br /></p><p>\n',
        'output': '\n<p>\n<b>Saida</b><br /></p><p>\n',
        'notes': '\n<p>\n<b>Notas</b><br /></p><p>\n'
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

    with open(directory+'/type', 'r') as sol_file:
        solutiontype = sol_file.read()
    # Insere a solução na questão
    name_dir = os.listdir(directory+'/solutions/')
    namesolution = name_dir[0]

    # Insere a linguagem de programação utilizada
    root.find("coderunnertype").text = solutiontype

    with open(directory+'/solutions/' + namesolution, 'r') as solution:
        root.find("answer").append(CDATA(solution.read()))

    # Faz uma busca por todos os arquivos de teste e os ordena
    tests = os.listdir(directory+'/testcases/')
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
            with open(directory+'/testcases/'+arq, 'r') as testout:
                testoroot.find("expected").find("text").text = testout.read()

                if arq in list_tests_show:
                    testoroot.set("useasexample", "1")

                root.find("testcases").append(testoroot)

                testtree = ET.parse(package_dir + 'Testcase-Template.xml')
                testoroot = testtree.getroot()
        else:
            with open(directory+'/testcases/'+arq, 'r') as testinput:
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
    with open(directory+'/time', 'r') as time_file:
        root.find("cputimelimitsecs").text = time_file.read()
    with open(directory+'/memory', 'r') as memory_file:
        root.find("memlimitmb").text = memory_file.read()

    # Gera o arquivo final da questão
    files = 'Files'
    if not os.path.exists(files):
        os.mkdir(files)
    tree.write(files + '/' + question_name + '.xml', 'UTF-8')
