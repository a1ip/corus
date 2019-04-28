
import tarfile
from datetime import datetime

from ..record import Record
from ..io import (
    parse_csv,
    skip_header,
)


class BuriyRecord(Record):
    __attributes__ = ['timestamp', 'url', 'edition', 'topics', 'title', 'text']

    def __init__(self, timestamp, url, edition, topics, title, text):
        self.timestamp = timestamp
        self.url = url
        self.edition = edition
        self.topics = topics
        self.title = title
        self.text = text


def load_tar(path):
    with tarfile.open(path) as tar:
        for member in tar:
            if not member.isfile():
                continue
            yield tar.extractfile(member)


def parse_lines(file, encoding='utf8'):
    for line in file:
        yield line.decode(encoding)


def parse_timestamp(timestamp):
    for pattern in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
        try:
            return datetime.strptime(timestamp, pattern)
        except ValueError:
            continue


def maybe_none(value, none=('',)):
    if value in none:
        return
    return value


def parse_buriy(lines, max_text=300000):
    rows = parse_csv(lines, max_field=max_text)
    skip_header(rows)
    for row in rows:
        timestamp, url, edition, topics, title, text = row
        timestamp = parse_timestamp(timestamp)
        edition = maybe_none(edition, ('', '-'))
        topics = maybe_none(topics)
        yield BuriyRecord(
            timestamp=timestamp,
            url=url,
            edition=edition,
            topics=topics,
            title=title,
            text=text
        )


def load_buriy(path):
    for file in load_tar(path):
        lines = parse_lines(file)
        for record in parse_buriy(lines):
            yield record


load_buriy_lenta = load_buriy
load_buriy_news = load_buriy
load_buriy_webhose = load_buriy


__all__ = [
    'load_buriy_lenta',
    'load_buriy_news',
    'load_buriy_webhose'
]
