
from ..record import Record
from ..io import (
    load_gz_lines,
    parse_csv
)
)


class LentaRecord(Record):
    __attributes__ = ['url', 'title', 'text', 'topic', 'tags']

    def __init__(self, url, title, text, topic, tags):
        self.url = url
        self.title = title
        self.text = text
        self.topic = topic
        self.tags = tags


def parse(lines):
    rows = parse_csv(lines)
    for cells in rows:
        yield LentaRecord(*cells)


def load(path):
    lines = load_gz_lines(path)
    return parse(lines)
