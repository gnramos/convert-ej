import re


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
        r'\`\`': '\"',
        r'\'\'': '\"',
        #  r'\\leq': '&le;',
        #  r'\\le': '&le;',
        #  r'\\geq': '&ge;',
        #  r'\\ge': '&ge;',
        #  r'\\lt': '&lt;',
        #  r'\\gt': '&gt;',
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

    s = re.sub(r'\$([^\$]*)\$', r'\\( \1 \\)', s)
    s = re.sub(r'\$\$([^\$]*)\$\$', r'<p><br />\\( \1 \\)<br /></p>', s)

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
