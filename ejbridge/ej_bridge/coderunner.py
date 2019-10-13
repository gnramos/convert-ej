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
    return '\n<p>\n<b>' + sec_name + '</b><br />\n' + description + '\n</p>\n'


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
        xmlname = root.find("name").find("text")
        xmlname.text = name.read()

    sections = {
        'legend': '',
        'input': 'Entrada',
        'output': 'Saida',
        'notes': 'Notas'
    }
    # Formata os textos
    for file_name, sec_name in sections.items():
        if os.path.isfile(dir_sec + file_name + '.tex'):
            texto += get_section(dir_sec + file_name + '.tex', sec_name)

    # Insere o texto
    xmlquestion = root.find("questiontext").find("text")
    xmlquestion.append(CDATA(texto))

    # Insere a solução na questão
    name_dir = os.listdir(directory+'/solutions/')
    for name in name_dir:
        if name.endswith('.cpp') or name.endswith('.c'):
            namesolution = name

    with open(directory+'/solutions/' + namesolution, 'r') as solution:
        xmlsolution = root.find("answer")
        xmlsolution.append(CDATA(solution.read()))

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
            with open(directory+'/tests/'+arq, 'r') as testoutput:
                xmloutput = testoroot.find("expected").find("text")
                xmloutput.text = testoutput.read()

                if arq in list_tests_show:
                    testoroot.set("useasexample", "1")

                xmltestcases = root.find("testcases")
                xmltestcases.append(testoroot)

                testtree = ET.parse(package_dir + 'Testcase-Template.xml')
                testoroot = testtree.getroot()
        else:
            with open(directory+'/tests/'+arq, 'r') as testinput:
                xmlinput = testoroot.find("stdin").find("text")
                xmlinput.text = testinput.read()

    # Insere as tags
    with open(directory+"/tags", 'r') as tagfile:
        tagscontent = tagfile.readlines()
    taglist = [x.strip() for x in tagscontent]

    tags = root.find("tags")
    for tagelement in taglist:
        tag = ET.Element('tag')
        tagtext = ET.SubElement(tag, 'text')
        tagtext.text = tagelement
        tags.append(tag)

    # Gera o arquivo final da questão
    files = 'Files'
    if not os.path.exists(files):
        os.mkdir(files)
    tree.write(files + '/' + question_name + '.xml')


def dir_xml_gen(directory):
    questions = os.listdir(directory)
    for name in questions:
        xml_gen(directory + '/' + name, name)
