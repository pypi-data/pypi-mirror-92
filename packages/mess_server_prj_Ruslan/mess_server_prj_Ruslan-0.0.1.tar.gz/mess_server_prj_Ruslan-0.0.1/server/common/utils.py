"""Functions for sending and receiving messages"""
import json

from .vars import ENCODING, MAX_PACKAGE_LENGTH


def send_message(sock, msg):
    """
    Sending message function
    :param sock:
    :param msg:
    :return:
    """
    msg_js = json.dumps(msg)
    msg_encoded = msg_js.encode(ENCODING)
    sock.send(msg_encoded)


def receive_message(sock):
    """
    Receiving message function
    :param sock:
    :return:
    """
    response_encoded = sock.recv(MAX_PACKAGE_LENGTH)
    if isinstance(response_encoded, bytes):
        response_js = response_encoded.decode(ENCODING)
        response = json.loads(response_js)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError
