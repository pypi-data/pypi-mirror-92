"""
The BBDB parser.
"""

from lark import Lark, Transformer
from typing import Optional, List
from pathlib import Path


def parse(text: str, parser: Optional[Lark] = None):
    """Parse some text using a Lark parser.
    """

    parser = parser or make_parser()
    return parser.parse(text)


def make_parser(grammarfile: str = "bbdb.lark") -> Lark:
    """Build a Lark parser using a grammar file.
    """

    dirname = Path(__file__).parent
    filename = dirname / grammarfile
    grammar = filename.read_text()

    return Lark(grammar, start="records", parser="lalr",
                transformer=BBDBTransformer())


class BBDBTransformer(Transformer):
    """Transform parsed tree into a dictionary.
    """

    _recfields = ('firstname', 'lastname', 'affix', 'aka', 'company', 'phone',
                  'address', 'net', 'notes', 'uuid', 'creation', 'timestamp')

    _addrfields = ('tag', 'location', 'city', 'state', 'zipcode', 'country')

    def records(self, items):
        return {"records": items}

    def record(self, items):
        return map_fields(self._recfields, items)

    def address(self, items):
        data = {}
        if items[0]:
            for item in items:
                key = item.pop('tag')
                data[key] = item

        return data

    def address_record(self, items):
        return map_fields(self._addrfields, items)

    def pairs(self, items):
        data = {}
        if items[0]:
            for item in items:
                key, value = item.children
                data[key] = value

        return data

    def string(self, items):
        return items[0][1:-1].replace(r'\"', '"')

    net = lambda self, elt: elt if elt[0] else []
    number = lambda self, elt: int(elt[0])
    atom = lambda self, elt: str(elt[0])
    none = lambda self, elt: ""

    notes = phone = pairs
    streets = phone_usa = list
    cache = none


def map_fields(names: List[str], items: list):
    return {tag: items[i] for i, tag in enumerate(names)}
