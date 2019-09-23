import xml.etree.ElementTree as ET
import os


# Lida provisoriamente com a tradução do texto em tex
# para html
# Será substituido posteriormente por uma abordagem
# utilizando expressões regulares
def tex2html(s):
    s = s.replace("\\begin{itemize}", "<ul>")
    s = s.replace("\\end{itemize}", "</ul>")
    s = s.replace("\\item", "<br />")
    s = s.replace("\\InputFile", "<br /><br />Entradas:<br /><br />")
    s = s.replace("\\OutputFile", "<br /><br />Saídas:<br /><br />")
    s = s.replace("\\^", "^")
    s = s.replace("\\ge", "&#8805;")
    s = s.replace("\\geq", "&#8805;")
    s = s.replace("\\leq", "&#8804;")
    s = s.replace("\\le", "&#8804;")
    s = s.replace("$", " ")
    s = s.replace("\\arrowvert", "|")
    s = s.replace("\\Examples", "<br /><br />")

    return s


# Templates para a questão e para casos teste
tree = ET.parse('Template.xml')
root = tree.getroot()
root = root[0]
testtree = ET.parse('Testcase-Template.xml')
testoroot = testtree.getroot()

directory = 'ed'  # Nome do diretório

# Insere o nome da questão
with open(directory+'/statement-sections/english/name.tex', 'r') as name:
    xmlname = root.find("name")
    xmltextname = xmlname.find("text")
    xmltextname.text = name.read()

# Modifica e insere o texto da questão
with open(directory+'/statements/english/problem.tex', 'r') as question:
    xmlquestion = root.find("questiontext")
    xmltextquestion = xmlquestion.find("text")
    xmltextquestion.text = tex2html(question.read())

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
            xmloutput = testoroot.find("expected")
            xmltextoutput = xmloutput.find("text")
            xmltextoutput.text = testoutput.read()

            xmltestcases = root.find("testcases")
            xmltestcases.append(testoroot)
    else:
        with open(directory+'/tests/'+arq, 'r') as testinput:
            xmlinput = testoroot.find("testcode")
            xmltextinput = xmlinput.find("text")
            xmltextinput.text = testinput.read()

# Gera o arquivo final da questão
tree.write('Problem.xml')
