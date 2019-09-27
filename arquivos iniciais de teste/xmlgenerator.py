import xml.etree.ElementTree as ET
import os
import re


def spacei():
    return '\n\n<br /><br />'


def spacef():
    return '<br /><br />\n\n'


# Lida parcialmente com a tradução do texto em tex para html
def tex2html(s):
    """
    Return a string with syntax substitutions,
    from latex format to html, performed on the
    given input

    rules -- dict with all the substiturion rules
             for a specific format
    s -- input string to be formated
    """
    rules1 = {
        r'\\begin{itemize}': '<ul>',
        r'\\end{itemize}': '</ul>',
        r'\\lt': '&lt;',
        r'\\le': '&le;',
        r'\\gt': '&gt;',
        r'\\ge': '&ge;',
        r'\\arrowvert': '|',
        r'\\\^': '^'
    }

    rules2 = {
        r'\\emph': 'i',
        r'\\textbf': 'b',
        r'\\textit': 'i'
        # r'\\textsc': '',
        # r'\\texttt': '',
        # r'\\textsf': '',
        # r'\\textrm': '',
        # r'\\textsl': ''
    }

    rules3 = {
        r'\\item': 'li'
    }

    for l, h in rules1.items():
        s = re.sub(l, h, s)

    for l, h in rules2.items():
        l_str = r'%s{([^}]*)}' % l
        h_str = r'<%s>\1</%s>' % (h, h)
        s = re.sub(l_str, h_str, s)

    for l, h in rules3.items():
        l_str = r'%s([^\n]*)' % l
        h_str = r'<%s>\1</%s>' % (h, h)
        s = re.sub(l_str, h_str, s)

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
    texto = '<h1>'+texto+'</h1>'+spacef()

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
