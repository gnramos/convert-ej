import xml.etree.ElementTree as ET


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


text = "TESTE"

text2 = "ola eu sou uma solução"
tree = ET.parse('Template.xml')
root = tree.getroot()
root = root[0]
xmlquestion = root.find("questiontext").find("text")
xmlsolution = root.find("answer")


xmlquestion.append(CDATA(text))
xmlsolution.append(CDATA(text2))

tree.write('resultado.xml')
