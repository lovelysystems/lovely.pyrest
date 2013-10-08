from docutils.core import publish_doctree
from docutils import nodes
import sys


def create_node(text):
    """
    Converts a reStructuredText String into a docutils.node
    This node can be included in the document.
    """
    return publish_doctree(text).children


def trim(docstring):
    """
    Removes spaces and extra tabs from a docstring
    Implementation from http://www.python.org/dev/peps/pep-0257/
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    res = '\n'.join(trimmed)
    if not isinstance(res, unicode):
        res = res.decode('utf8')
    return res


def empty_node():
    return nodes.inline(text="")
