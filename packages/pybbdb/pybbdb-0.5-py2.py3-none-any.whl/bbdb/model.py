"""
The BBDB model.
"""

from __future__ import annotations

import sys

from pydantic import BaseModel, Field, ValidationError, validator
from typing import List, Dict, Union, Iterator, IO
from functools import total_ordering
from datetime import datetime
from uuid import UUID, uuid4

from .timestamp import to_datestamp, from_datestamp, now
from .parser import parse


PhoneNumber = Union[str, List[int]]


class BBDBModel(BaseModel):
    """Base BBDB data model.
    """

    def check(self) -> None:
        """Check object is valid, or raise ValueError.
        """

        try:
            d = self.dict()
            self.__class__(**d)
        except ValidationError as exc:
            raise ValueError(str(exc))

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
            UUID: lambda v: str(v),
        }


class Address(BBDBModel):
    """A BBDB address.
    """

    location: List[str] = []
    city: str = ""
    state: str = ""
    zipcode: str = ""
    country: str = ""

    def set_location(self, *location: str) -> None:
        """Set list of location lines.
        """

        self.location = list(location)

    def outputs(self) -> Iterator[str]:
        """Yield lisp output for this item.
        """

        if self.location:
            yield "(" + " ".join(map(quote, self.location)) + ")"
        else:
            yield "nil"

        for attr in 'city', 'state', 'zipcode', 'country':
            yield quote(getattr(self, attr))

    def __str__(self) -> str:
        parts = list(self.location)

        for attr in "city", "state", "zipcode", "country":
            value = getattr(self, attr)
            if value:
                parts.append(value)

        return ", ".join(parts)


@total_ordering
class Record(BBDBModel):
    """A BBDB record.
    """

    firstname: str = ""
    lastname: str = ""
    affix: str = ""
    aka: str = ""
    company: str = ""
    phone: Dict[str, PhoneNumber] = {}
    address: Dict[str, Address] = {}
    net: List[str] = []
    notes: Dict[str, str] = {}
    uuid: UUID = Field(default_factory=uuid4)
    creation: datetime = Field(default_factory=now)
    timestamp: datetime = Field(default_factory=now)

    @validator("uuid", pre=True)
    def convert_uuid(cls, v: Union[str, UUID]) -> UUID:
        if isinstance(v, str):
            return UUID(v)
        else:
            return v

    @validator("creation", "timestamp", pre=True)
    def convert_datetime(cls, v: Union[str, datetime]) -> datetime:
        if isinstance(v, str):
            return from_datestamp(v)
        else:
            return v

    @property
    def name(self) -> str:
        """Composite name property.
        """

        parts = [self.firstname or "", self.lastname or ""]
        parts = [p for p in parts if p]
        return " ".join(parts)

    def set_name(self, first: str = "", last: str = "") -> None:
        """Set the first and last names.
        """

        self.firstname = first or ""
        self.lastname = last or ""

    def add_phone(self, tag: str, number: PhoneNumber) -> None:
        """Add a phone number entry.
        """

        self.phone[tag] = number

    def add_address(self, tag: str, *location: str, **kw) -> Address:
        """Add an address entry.
        """

        address = Address(location=list(location), **kw)
        self.address[tag] = address
        return address

    def add_net(self, *names: str) -> None:
        """Add a network address entry.
        """

        self.net.extend(names)

    def add_note(self, tag: str, text: str) -> None:
        """Add a notes entry.
        """

        self.notes[tag] = text.replace("\n", r'\n')

    def outputs(self) -> Iterator[str]:
        """Yield lisp output for this item.
        """

        for attr in 'firstname', 'lastname':
            value = getattr(self, attr)
            if value:
                yield quote(value)
            else:
                yield "nil"

        for attr in 'affix', 'aka', 'company':
            value = getattr(self, attr)
            if value:
                yield "(" + quote(value) + ")"
            else:
                yield "nil"

        if self.phone:
            rec = []
            for tag, number in sorted(self.phone.items()):
                if isinstance(number, str):
                    number = quote(number)
                else:
                    number = " ".join(map(str, number))
                rec.append("[" + quote(tag) + " " + number + "]")
            yield "(" + " ".join(rec) + ")"
        else:
            yield "nil"

        if self.address:
            rec = []
            for tag, address in sorted(self.address.items()):
                addr = " ".join(list(address.outputs()))
                rec.append("[" + quote(tag) + " " + addr + "]")
            yield "(" + " ".join(rec) + ")"
        else:
            yield "nil"

        if self.net:
            yield "(" + " ".join(map(quote, sorted(self.net))) + ")"
        else:
            yield "nil"

        if self.notes:
            rec = []
            for tag, text in sorted(self.notes.items()):
                rec.append("(" + tag + " . " + quote(text) + ")")
            yield "(" + " ".join(rec) + ")"
        else:
            yield "nil"

        yield quote(str(self.uuid))
        yield quote(to_datestamp(self.creation))
        yield quote(to_datestamp(self.timestamp, time=True))

        yield "nil"

    def __lt__(self, other) -> bool:
        return list(self) < list(other)


class BBDB(BBDBModel):
    """A BBDB database.
    """

    coding: str = "utf-8-emacs"
    fileversion: int = 9
    records: List[Record] = []

    def add_record(self, first: str = "", last: str = "", **kw) -> Record:
        rec = Record(firstname=first, lastname=last, **kw)

        self.records.append(rec)
        self.records.sort()

        return rec

    @property
    def userfields(self) -> list:
        fields = set()
        for rec in self.records:
            for tag in rec.notes:
                fields.add(tag)

        return list(sorted(fields))

    @staticmethod
    def fromfile(path: str) -> BBDB:
        """Read and return BBDB from a file.
        """

        db = BBDB()
        db.read_file(path)
        return db

    @staticmethod
    def frombuffer(buf: IO) -> BBDB:
        """Read and return BBDB from a text stream.
        """

        db = BBDB()
        db.read(buf)
        return db

    @staticmethod
    def fromdict(d: Dict) -> BBDB:
        """Parse and return BBDB from a dict.
        """

        return BBDB.parse_obj(d)

    def read(self, f: IO = sys.stdin) -> None:
        """Read and append BBDB records from a stream.
        """

        text = f.read()
        data = parse(text)
        recdata = data["records"]
        records = [Record(**rec) for rec in recdata]
        self.records.extend(records)

    def read_file(self, path: str) -> None:
        """Read and append BBDB records from a file.
        """

        with open(path) as f:
            self.read(f)

    def write(self, f: IO = sys.stdout) -> None:
        """Write database to a text stream.
        """

        f.write(self.lisp())

    def write_file(self, path: str) -> None:
        """Write database to a file.
        """

        with open(path, "w") as f:
            self.write(f)

    def lisp(self) -> str:
        """Return emacs-lisp representation of the database.
        """

        return "".join(self.outputs())

    def outputs(self) -> Iterator[str]:
        """Yield lisp output for this item.
        """

        yield ";; -*-coding: %s;-*-\n" % self.coding
        yield ";;; file-version: %d\n" % self.fileversion

        if self.userfields:
            yield ";;; user-fields: (%s)\n" % " ".join(self.userfields)

        for rec in sorted(self.records):
            yield "["
            yield " ".join(list(rec.outputs()))
            yield "]\n"

    def __repr__(self) -> str:
        return "<BBDB: %d records>" % len(self.records)


def quote(string: str) -> str:
    return '"' + string.replace('"', r'\"') + '"'
