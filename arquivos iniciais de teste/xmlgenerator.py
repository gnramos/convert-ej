import xml.etree.ElementTree as ET
import os
import re


def spacei():
    return '\n\n<br /><br />'


def spacef():
    return '<br /><br />\n\n'


# Lida parcialmente com a tradução do texto em tex para html
def tex2html(s):
    s = re.sub(r"\\begin{itemize}", "<ul>", s)
    s = re.sub(r"\\end{itemize}", "</ul>", s)
    s = re.sub(r"\\ge", "&#8805;", s)
    s = re.sub(r"\\geq", "&#8805;", s)
    s = re.sub(r"\\le", "&#8804;", s)
    s = re.sub(r"\\leq", "&#8804;", s)
    s = re.sub(r"\\arrowvert", "|", s)
    s = re.sub(r"\\^", "^", s)

    return s


# Templates para a questão e para casos teste
tree = ET.parse('Template.xml')
root = tree.getroot()
root = root[0]
testtree = ET.parse('Testcase-Template.xml')
testoroot = testtree.getroot()

directory = 'ed'  # Nome do diretório

texto = ''  # Texto da questão

# Insere o nome da questão
with open(directory+'/statement-sections/english/name.tex', 'r') as name:
    texto = name.read()
    xmlname = root.find("name").find("text")
    xmlname.text = texto
    texto += spacef()

# Armazena e modifica os textos
with open(directory+'/statement-sections/english/legend.tex', 'r') as question:
    texto += spacei() + tex2html(question.read())

with open(directory+'/statement-sections/english/input.tex', 'r') as question:
    texto += spacei()+'Entrada:'+spacef() + tex2html(question.read())

with open(directory+'/statement-sections/english/output.tex', 'r') as question:
    texto += spacei()+'Saída:'+spacef() + tex2html(question.read())

# Insere o texto
xmlquestion = root.find("questiontext")
xmltextquestion = xmlquestion.find("text")
xmltextquestion.text = texto

# Insere a solução na questão
namesolution = 'ed-pilha-infix2posfix.cpp'
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
