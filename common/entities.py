from dataclasses import dataclass
from enum import Enum

from dataclasses_jsonschema import JsonSchemaMixin


class Color(Enum):
    RED = 'FF0000'
    GREEN = '00FF00'
    BLUE = '0000FF'
    GRAY = '555555'


@dataclass
class Attachment(JsonSchemaMixin):
    color: Color
    title: str
    text: str = None


@dataclass
class Message(JsonSchemaMixin):
    channel: str
    attachments: list[Attachment] = None
    text: str = None

