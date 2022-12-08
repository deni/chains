import base64
import json


def base64_string(bytes):
    bytes_base64 = base64.b64encode(bytes)
    string = bytes_base64.decode('utf-8')

    return string


def json_serialize_canonical(object):
    serialized = json.dumps(object,
        sort_keys = True,
        indent = None,
        separators = (',', ':'),
        ensure_ascii = False,
        allow_nan = False,
    )

    return serialized
