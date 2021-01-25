import typing
from dataclasses import dataclass

from dataclasses_json import dataclass_json


#
# Flyte supports passing JSON's between tasks. But, to simplify the
# usage for the users and introduce type-safety, flytekit supports
# passing custom data objects between tasks. Currently only
# dataclasses that are decorated with @dataclasses_json are supported.
#


#
# The Context is a user defined complex type, which can be used to
# pass complex data between tasks.  Moreover, this data can be sent
# between different languages and also input through the Flyteconsole
# as a raw JSON.
#
# Only other supported types can be nested in this class, for example
# it can only contain other ``@dataclass_json`` annotated dataclasses
# if you want to use complex classes. Arbitrary classes will cause a
# **failure**.
#
# All variables in DataClasses should be **annotated with their
# type**. Failure to do should will result in an error

@dataclass_json
@dataclass
class User(object):
    name: str
    email: str


@dataclass_json
@dataclass
class DataLake(object):
    pass


@dataclass_json
@dataclass
class ADLGen2(DataLake):
    pass


@dataclass_json
@dataclass
class IFracFileHandle(object):
    name: str
    lake: DataLake


@dataclass_json
@dataclass
class Parameters(object):
    pass


@dataclass_json
@dataclass
class DecomposedIFracFileHandle(object):
    location: str
    parameters: Parameters
    filenames: typing.List[str]


@dataclass_json
@dataclass
class Platform(object):
    pass


@dataclass_json
@dataclass
class AWS(Platform):
    pass


@dataclass_json
@dataclass
class Azure(Platform):
    pass


@dataclass_json
@dataclass
class Context(object):
    user: User
    platform: Platform
