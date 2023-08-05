from ..simple_parsing import ArgumentParser, field, subparsers
from ..simple_parsing.helpers import Serializable
from dataclasses import dataclass

@dataclass
class Dependency(Serializable):
    name:                str = ''
    gradle_placeholder:  str = ''

@dataclass
class Module(Serializable):
    name:                        str  = ''
    alias:                       str  = ''
    path:                        str  = ''
    build:                       str = ''
    upload_version:              str = ''
    upload_version_placeholder:  str = ''
    dependencies:                list[Dependency] = field(default_factory=list)

@dataclass
class Config(Serializable):
    suffix:              str = ''
    outputs:             str = ''
    projects:            list[Module] = field(default_factory=list)
