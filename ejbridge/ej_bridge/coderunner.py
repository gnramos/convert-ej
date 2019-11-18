import xml.etree.ElementTree as ET
import os
import subprocess
from base64 import b64encode
from .t2h import tex2html


def CDATA(text=None):
    '''
    Includes the CDATA tag
    '''
    element = ET.Element('![CDATA[')
    element.text = text
    return element


ET._original_serialize_xml = ET._serialize_xml


def _serialize_xml(write, elem, qnames, namespaces,
                   short_empty_elements, **kwargs):
    '''
    New serializing function to deal with the CDATA tag
    '''
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


def get_templates(package_dir):
    '''
    Return the imported data opened from the templates
    '''
    tree = ET.parse(os.path.join(package_dir, 'Template.xml'))
    root = tree.getroot()
    root = root[0]
    test_tree = ET.parse(os.path.join(package_dir, 'Testcase-Template.xml'))
    test_root = test_tree.getroot()

    return [tree, root, test_tree, test_root]


def insert_name(dir_text, root):
    with open(os.path.join(dir_text, 'name.tex'), 'r') as name:
        root.find("name").find("text").text = name.read()


def insert_texts(dir_text, root):
    sections = {
        'legend': '<p>',
        'input': '\n<p>\n<b>Entrada</b><br /></p><p>\n',
        'output': '\n<p>\n<b>Saida</b><br /></p><p>\n',
        'notes': '\n<p>\n<b>Notas</b><br /></p><p>\n'
    }
    texto = ''

    for file_name, sec_name in sections.items():
        if os.path.isfile(os.path.join(dir_text, file_name + '.tex')):
            texto += get_section(os.path.join(dir_text, file_name + '.tex'),
                                 sec_name)

    root.find("questiontext").find("text").append(CDATA(texto))


def convert_eps_to_png(dir_text):
    files_sec = os.listdir(dir_text)
    for name in files_sec:
        if name.endswith('.eps'):
            subprocess.call(['convert', os.path.join(dir_text, name),
                             '+profile', '"*"',
                             os.path.join(dir_text, name[:-4] + '.png')])


def insert_images(dir_text, root):
    files_sec = os.listdir(dir_text)
    for name in files_sec:
        if name.endswith('.jpg') or name.endswith('.png'):
            img = ET.Element('file')
            img.set('name', name)
            img.set('path', '/')
            img.set('encoding', 'base64')

            with open(os.path.join(dir_text, name), "rb") as image:
                encoded_string = str(b64encode(image.read()), 'utf-8')

            img.text = encoded_string
            root.find("questiontext").append(img)


def insert_tutorial(dir_text, root):
    if os.path.isfile(os.path.join(dir_text, 'tutorial.tex')):
        with open(os.path.join(dir_text, 'tutorial.tex'), 'r') as t:
            root.find("generalfeedback").find("text").text = tex2html(t.read())


def insert_solution_type(directory, root):
    with open(os.path.join(directory, 'type'), 'r') as sol_file:
        solutiontype = sol_file.read()
    root.find("coderunnertype").text = solutiontype


def insert_solution(directory, root):
    name_dir = os.listdir(os.path.join(directory, 'solutions'))
    namesolution = name_dir[0]
    with open(os.path.join(directory, 'solutions', namesolution), 'r') \
            as solution:
        root.find("answer").append(CDATA(solution.read()))


def get_example_testecases(dir_text):
    list_example_tests = []
    tests_show = os.listdir(dir_text)
    for arq in tests_show:
        if arq.endswith('.a'):
            list_example_tests.append(arq[8:])

    return list_example_tests


def insert_testcases(dir_text, directory, root,
                     test_root, package_dir):

    tests = os.listdir(os.path.join(directory, 'testcases'))
    tests.sort()

    list_example_tests = get_example_testecases(dir_text)

    for arq in tests:
        if arq.endswith('.a'):
            with open(os.path.join(directory, 'testcases', arq), 'r') \
                    as testout:
                test_root.find("expected").find("text").text = testout.read()

                if arq in list_example_tests:
                    test_root.set("useasexample", "1")

                root.find("testcases").append(test_root)

                test_tree = ET.parse(os.path.join(package_dir,
                                                  'Testcase-Template.xml'))
                test_root = test_tree.getroot()
        else:
            with open(os.path.join(directory, 'testcases', arq), 'r') \
                    as testinput:
                test_root.find("stdin").find("text").text = testinput.read()


def insert_tags(directory, root):
    with open(os.path.join(directory, "tags"), 'r') as tagfile:
        tagscontent = tagfile.readlines()
    taglist = [x.strip() for x in tagscontent]

    tags = root.find("tags")
    for tagelement in taglist:
        tag = ET.Element('tag')
        ET.SubElement(tag, 'text').text = tagelement
        tags.append(tag)


def insert_time_limit(directory, root):
    with open(os.path.join(directory, 'time'), 'r') as time_file:
        root.find("cputimelimitsecs").text = time_file.read()


def insert_memory_limit(directory, root):
    with open(os.path.join(directory, 'memory'), 'r') as memory_file:
        root.find("memlimitmb").text = memory_file.read()


def insert_penalty(root, penalty):
    root.find("penaltyregime").text = str(penalty)


def insert_all_or_nothing(root, all_or_nothing):
    root.find("allornothing").text = str(all_or_nothing)


def write_xml_file(tree, question_name):
    files = 'files'
    if not os.path.exists(files):
        os.mkdir(files)
    tree.write(os.path.join(files, question_name + '.xml'), 'UTF-8')


def intermediate_to_coderunner(directory, question_name,
                               penalty, all_or_nothing):

    # Templates para a questão e para casos teste
    package_dir = os.path.abspath(os.path.dirname(__file__))
    [tree, root, test_tree, test_root] = get_templates(package_dir)

    dir_text = os.path.join(directory, 'text')  # Diretório dos textos

    # Insere o nome
    insert_name(dir_text, root)

    # Insere os textos
    insert_texts(dir_text, root)

    # Converte imagens em .eps para .png
    convert_eps_to_png(dir_text)

    # Transforma imagens .png e .jpg em base64 e as insere no xml
    insert_images(dir_text, root)

    # Insere tutorial
    insert_tutorial(dir_text, root)

    # Insere o tipo da questão
    insert_solution_type(directory, root)

    # Insere a solução da questão
    insert_solution(directory, root)

    # Insere os testcases no template
    # e adiciona-o na questão
    insert_testcases(dir_text, directory, root,
                     test_root, package_dir)

    # Insere as tags
    insert_tags(directory, root)

    # Insere tempo e mémoria limite
    insert_time_limit(directory, root)
    insert_memory_limit(directory, root)

    # Insere argumentos de penalidade e allornothing
    insert_penalty(root, penalty)
    insert_all_or_nothing(root, all_or_nothing)

    # Gera o arquivo final da questão
    write_xml_file(tree, question_name)
