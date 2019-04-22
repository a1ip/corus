
import re

from ..record import Record
from ..io import load_gz_lines


class LibrusecRecord(Record):
    __attributes__ = ['id', 'text']

    def __init__(self, id, text):
        self.id = id
        self.text = text


def flush(id, buffer):
    return LibrusecRecord(id, '\n'.join(buffer))


def parse(lines):
    id = None
    buffer = []
    for line in lines:
        match = re.match(r'^(\d+)\.fb2', line)
        if match:
            if id:
                yield flush(id, buffer)
                buffer = []
            id = match.group(1)
            line = line[match.end() + 1:]  # extra space
        buffer.append(line)
    yield flush(id, buffer)


def load(path):
    lines = load_gz_lines(path)
    return parse(lines)
