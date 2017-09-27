# -*- coding: utf-8 -*-
import sys
PY2 = sys.version_info[0] == 2

# https://raw.githubusercontent.com/lepture/flask-wtf/master/flask_wtf/_compat.py

if not PY2:  # pragma: no cover
    unicode = str  # needed for pyflakes in py3

if PY2:  # pragma: nocover

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    text_type = unicode
    string_types = (str, unicode)

else:  # pragma: nocover

    def iteritems(d):
        return iter(d.items())

    def itervalues(d):
        return iter(d.values())

    text_type = str
    string_types = (str,)

def to_bytes(text):
    """Transform string to bytes."""
    if isinstance(text, text_type):
        text = text.encode('utf-8')
    return text


def to_unicode(input_bytes, encoding='utf-8'):
    """Decodes input_bytes to text if needed."""
    if not isinstance(input_bytes, string_types):
        input_bytes = input_bytes.decode(encoding)
    return input_bytes

