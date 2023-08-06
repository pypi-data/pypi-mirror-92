#  SPDX-License-Identifier: CC-BY-SA-4.0
"""
Python Package for controlling Alexa devices (echo dot, etc) programmatically.

This is code borrowed from stack overflow.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""
import socket


# https://stackoverflow.com/questions/2838244/get-open-tcp-port-in-python/2838309#2838309
def get_open_port() -> int:
    """Get random port.

    Returns
        int: open port

    """

    # pylint: disable=invalid-name

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
