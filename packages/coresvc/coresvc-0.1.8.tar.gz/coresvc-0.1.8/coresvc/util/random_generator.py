import random
import string
from uuid import uuid4


def gen_id() -> str:
    return str(uuid4())


def gen_string(length=32) -> str:
    return "".join(random.choices(string.ascii_letters, k=length))


def gen_float() -> float:
    pass


def gen_int() -> int:
    pass
