# Dynamo Dao

Typed library for interacting with DynamoDb tables.

## Installation

Available on [PyPI](https://pypi.org/project/dynamo-dao/)

```
pip install dynamo-dao
```

## Usage

The following example code shows some basic usage of this package. Note that the `ExampleDao` must define 4 abstract properties:

1. `table_name` - Name of the DynamoDb table resource (maps directly to what you'd see on the AWS console).
2. `unique_key` - The list of keys that together uniquely define an entry in the table.
3. `convert_to_dynamo` - A method which takes in the object and converts it to the entry in the DynamoDb table
4. `convert_from_dynamo` - The opposite of `convert_to_dynamo`

```
from typing import NamedTuple

from dynamo_dao import Dao, DynamoObject

class Example(NamedTuple):
    foo: str
    bar: int

class ExampleDao(Dao[Example]):
    table_name = "example"
    unique_key = ["foo"]

    def convert_to_dynamo(self, var: Example) -> DynamoObject:
        return {"foo": var.foo, "bar": var.bar}

    def convert_from_dynamo(self, var: DynamoObject) -> Example:
        return Example(foo=str(var["foo"]), bar=int(var["bar"]))


example_dao = ExampleDao()

example = Example(foo="hi", bar=1)

example_dao.create(example)
result = example_dao.read_one("foo", "hi")

assert example == result
```

## Why use?

The base dao is a [generic](https://mypy.readthedocs.io/en/stable/generics.html) object, which means child classes will benefit from type checking on functions like `read` and `create`.

In the example above, the type of `result` is `Example`.
