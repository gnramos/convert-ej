import xml.etree.ElementTree as ET
import os
from t2h import tex2html


def space(k):
    if k:
        return '<br /><br />\n\n'
    else:
        return '\n\n<br /><br />'


def xml_gen(directory):
    # Templates para a questão e para casos teste
    tree = ET.parse('Template.xml')
    root = tree.getroot()
    root = root[0]
    testtree = ET.parse('Testcase-Template.xml')
    testoroot = testtree.getroot()

    texto = ''  # Texto da questão
    stat_dir = '/statement-sections/english/'  # Diretório do texto

    # Insere o nome da questão
    with open(directory+stat_dir+'name.tex', 'r') as name:
        texto = name.read()
        xmlname = root.find("name").find("text")
        xmlname.text = texto
        texto = '<h1>'+texto+'</h1>'+space(1)

    # Armazena e modifica os textos
    with open(directory+stat_dir+'legend.tex', 'r') as question:
        texto += space(0) + tex2html(question.read())

    with open(directory+stat_dir+'input.tex', 'r') as question:
        texto += space(0)+'Entrada:'+space(1) + tex2html(question.read())

    with open(directory+stat_dir+'output.tex', 'r') as question:
        texto += space(0)+'Saída:'+space(1) + tex2html(question.read())

    # Insere o texto
    xmlquestion = root.find("questiontext")
    xmltextquestion = xmlquestion.find("text")
    xmltextquestion.text = texto

    # Insere a solução na questão
    name_dir = os.listdir(directory+'/solutions/')
    for name in name_dir:
        if name.endswith('.cpp'):
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
        else:
            with open(directory+'/tests/'+arq, 'r') as testinput:
                xmlinput = testoroot.find("testcode").find("text")
                xmlinput.text = testinput.read()

    # Gera o arquivo final da questão
    tree.write('Problem.xml')
