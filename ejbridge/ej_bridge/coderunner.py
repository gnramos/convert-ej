import xml.etree.ElementTree as ET
import os
from base64 import b64encode
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


def intermediate_to_coderunner(directory, question_name, penalty,
                               all_or_nothing, language):
    # Templates para a questão e para casos teste
    package_dir = os.path.abspath(os.path.dirname(__file__))
    tree = ET.parse(os.path.join(package_dir, 'Template.xml'))
    root = tree.getroot()
    root = root[0]
    testtree = ET.parse(os.path.join(package_dir, 'Testcase-Template.xml'))
    testoroot = testtree.getroot()

    texto = ''  # Texto da questão
    dir_sec = os.path.join(directory, 'text')  # Diretório do texto
    # Insere o nome
    with open(os.path.join(dir_sec, 'name.tex'), 'r') as name:
        root.find("name").find("text").text = name.read()

    sections = {
        'legend': '<p>',
        'input': '\n<p>\n<b>Entrada</b><br /></p><p>\n',
        'output': '\n<p>\n<b>Saida</b><br /></p><p>\n',
        'notes': '\n<p>\n<b>Notas</b><br /></p><p>\n'
    }
    # Formata os textos
    for file_name, sec_name in sections.items():
        if os.path.isfile(os.path.join(dir_sec, file_name + '.tex')):
            texto += get_section(os.path.join(dir_sec, file_name + '.tex'),
                                 sec_name)

    files_sec = os.listdir(dir_sec)
    for name in files_sec:
        if name.endswith('.jpg') or name.endswith('.png'):
            img = ET.Element('file')
            img.set('name', name)
            img.set('path', '/')
            img.set('encoding', 'base64')

            with open(os.path.join(dir_sec, name), "rb") as image:
                encoded_string = str(b64encode(image.read()), 'utf-8')

            img.text = encoded_string
            root.find("questiontext").append(img)

    # Insere o texto
    root.find("questiontext").find("text").append(CDATA(texto))

    # Insere tutorial
    if os.path.isfile(os.path.join(dir_sec, 'tutorial.tex')):
        with open(os.path.join(dir_sec, 'tutorial.tex'), 'r') as t:
            root.find("generalfeedback").find("text").text = tex2html(t.read())

    with open(os.path.join(directory, 'type'), 'r') as sol_file:
        solutiontype = sol_file.read()
    # Insere a solução na questão
    name_dir = os.listdir(os.path.join(directory, 'solutions'))
    namesolution = name_dir[0]

    # Insere a linguagem de programação utilizada
    root.find("coderunnertype").text = solutiontype

    with open(os.path.join(directory, 'solutions', namesolution), 'r') \
            as solution:
        root.find("answer").append(CDATA(solution.read()))

    # Faz uma busca por todos os arquivos de teste e os ordena
    tests = os.listdir(os.path.join(directory, 'testcases'))
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
            with open(os.path.join(directory, 'testcases', arq), 'r') \
                    as testout:
                testoroot.find("expected").find("text").text = testout.read()

                if arq in list_tests_show:
                    testoroot.set("useasexample", "1")

                root.find("testcases").append(testoroot)

                testtree = ET.parse(os.path.join(package_dir,
                                                 'Testcase-Template.xml'))
                testoroot = testtree.getroot()
        else:
            with open(os.path.join(directory, 'testcases', arq), 'r') \
                    as testinput:
                testoroot.find("stdin").find("text").text = testinput.read()

    # Insere as tags
    with open(os.path.join(directory, "tags"), 'r') as tagfile:
        tagscontent = tagfile.readlines()
    taglist = [x.strip() for x in tagscontent]

    tags = root.find("tags")
    for tagelement in taglist:
        tag = ET.Element('tag')
        ET.SubElement(tag, 'text').text = tagelement
        tags.append(tag)

    # Insere tempo e mémoria limite
    with open(os.path.join(directory, 'time'), 'r') as time_file:
        root.find("cputimelimitsecs").text = time_file.read()
    with open(os.path.join(directory, 'memory'), 'r') as memory_file:
        root.find("memlimitmb").text = memory_file.read()

    # Insere argumentos de penalidade e allornothing
    root.find("penaltyregime").text = str(penalty)
    root.find("allornothing").text = str(all_or_nothing)

    # Gera o arquivo final da questão
    files = 'Files'
    if not os.path.exists(files):
        os.mkdir(files)
    tree.write(os.path.join(files, question_name + '.xml'), 'UTF-8')
