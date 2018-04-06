import sys
import urllib


def url_encode(text):
    try:
        if (sys.version_info > (3, 0)):
            # Python 3 code in this block
            return urllib.parse.quote(text)
        else:
            # Python 2 code in this block
            return urllib.quote(text)
    except Exception as e:
        return text.replace(' ', '')


def url_decode(text):
    try:
        if (sys.version_info > (3, 0)):
            # Python 3 code in this block
            return urllib.parse.unquote(text)
        else:
            # Python 2 code in this block
            return urllib.unquote(text)
    except Exception as e:
        raise Exception