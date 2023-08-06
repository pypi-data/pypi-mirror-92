from datasette import hookimpl

import base64

def decode_base64(encodedText):
    dataBytes = base64.b64decode(encodedText)
    return dataBytes.decode('utf-8')

def encode_base64(rawText):
    messageData = rawText.encode('ascii')
    encodedString = base64.b64encode(messageData)
    return encodedString.decode('utf-8')


@hookimpl
def prepare_connection(conn):
    conn.create_function("base64decode", 1, decode_base64)
    conn.create_function("base64encode", 1, encode_base64)