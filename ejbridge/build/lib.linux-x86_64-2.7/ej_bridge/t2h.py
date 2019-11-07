import re


def tex2html(s):
    """
    Return a string with syntax substitutions,
    from LaTeX format to html, performed on the
    given input.

    Arguments:
    s -- input string to be formated
    """

    # Convert the mathematical equations
    s = re.sub(r'\$([^\$]*)\$', r'\\( \1 \\)', s)
    s = re.sub(r'\$\$([^\$]*)\$\$', r'<p><br />\\( \1 \\)<br /></p>', s)

    # Dict with all the substitution rules for a specific format
    rules1 = {
        r'\\begin{itemize}': '<ul>',
        r'\\end{itemize}': '</ul>',
        r'\\begin{center}': '<p style="text-align: center;">',
        r'\\end{center}': '</p>',
        r'\`\`': '\"',
        r'\'\'': '\"',
        r'\\arrowvert': '|',
        r'\\\^': '^',
        r'\n\n': '</p>\n\n<p>\n'
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

    # Apply the rules to the string
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
