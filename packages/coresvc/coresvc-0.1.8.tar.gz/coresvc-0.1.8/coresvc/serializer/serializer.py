"""Serialization utilities.

Supported codecs
================

* **json**    - json with UTF-8 encoding.
* **pickle**  - pickle with base64 encoding (not urlsafe).
* **msgpack**  - https://msgpack.org/
* **protobuf**  - https://developers.google.com/protocol-buffers/

Serialization by name
=====================

The :func:`dumps` function takes a codec name and the object to encode,
then returns bytes:

.. sourcecode:: pycon

    >>> s = dumps(obj, 'json')

For the reverse direction, the :func:`loads` function takes a codec
name and bytes to decode:

.. sourcecode:: pycon

    >>> obj = loads(s, 'json')
"""

import json
import pickle
from typing import Any

default_codec = 'json'


def dumps(obj: Any, codec: str = None) -> bytes:
    """Encode object into bytes."""
    codec = codec or default_codec

    if codec == 'json':
        return json.dumps(obj).encode()
    elif codec == 'pickle':
        return pickle.dumps(obj)


def loads(data: bytes, codec: str = None) -> Any:
    """Decode object from bytes."""
    codec = codec or default_codec

    if codec == 'json':
        return json.loads(data.decode())
    elif codec == 'pickle':
        return pickle.loads(data)
