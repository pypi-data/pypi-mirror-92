__all__ = [
    "Struct",
    "Object",
    "String",
    "Integer",
    "Double",
    "Boolean",
    "Array",
    "Map"
]

from typing import Type, Union, Tuple, Dict, List, Any
from itertools import zip_longest
import base64

class Schema:

    Map: Dict[str, "Schema.Base"] = {}

    class Meta(type):

        def __new__(cls, name: str, bases: Tuple[Union["Schema.Base", type], ...], namespace: Dict[str, Any]):
            return super().__new__(cls, name, bases, bases[0].build(namespace))

    class Base:

        name: str
        schemas: Dict[str, "Schema.Base"]

        @classmethod
        def build(cls, namespace: Dict[str, Any]) -> Dict[str, Any]:
            return {**{"schemas": {}}, **namespace}

        @classmethod
        def dump(cls):
            return {
                "type": cls.name
            }

        @classmethod
        def create(cls, value: Any) -> Any:
            return value

        @classmethod
        def pack(cls, value: Any) -> Any:
            return value

        @classmethod
        def make(cls, document: Dict[str, Any], schemas: Dict[str, "Schema.Object"]) -> "Schema.Base":
            raise NotImplementedError

    class Object:

        @classmethod
        def format(cls, value: Any) -> Any: ...

    class NonObject: ...

    @staticmethod
    def register(schema: Type["Schema.Base"]):
        Schema.Map.update({
            schema.name: schema
        })

    @staticmethod
    def select(object: Any, schemas: Dict[str, "Schema.Base"]) -> "Schema.Base":
        if isinstance(object, type):
            if object in Schema.Map:
                return Schema.Map[object]
            elif issubclass(object, Schema.Base):
                schemas.update(object.schemas)
                if issubclass(object, Schema.Object) and not issubclass(object, Schema.NonObject):
                    schemas[object.__name__] = object
                return object
        elif object in Schema.Map:
            return Schema.Map[object]
        elif isinstance(object, Schema.Base):
            return object
        assert 0, object
    
    @staticmethod
    def make(document: Dict[str, Any], schemas: Dict[str, "Schema.Object"]) -> "Schema.Base":
        return Schema.Map[document["type"]].make(document, schemas)

class Struct(Schema.Base, Schema.Object, metaclass = Schema.Meta):
    name = "struct"

    fields: Dict[str, Schema.Base]

    def __init__(self, *args, **kwargs) -> None:
        for info, value in zip_longest(self.fields.items(), args):
            name, _ = info
            if value is not None:
                kwargs[name] = value
            assert name in kwargs
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __setattr__(self, name: str, value: Any) -> None:
        assert name in self.fields
        super().__setattr__(name, self.fields[name].create(value))

    @classmethod
    def build(cls, namespace: Dict[str, Any]) -> Dict[str, Any]:
        schemas = namespace.setdefault("schemas", {})
        fields: Dict[str, "Schema"] = namespace.setdefault("fields", {})
        fields.update({key: Schema.select(value, schemas) for key, value in namespace.get("__annotations__", {}).items()})
        return namespace

    @classmethod
    def dump(cls) -> Dict[str, Any]:
        return {
            "type": cls.name,
            "ref": cls.__name__,
        }

    @classmethod
    def format(cls) -> Dict[str, Any]:
        return {
            "type": cls.name,
            "name": cls.__name__,
            "fields": {name: field.dump() for name, field in cls.fields.items()}
        }

    @classmethod
    def create(cls, value: Dict[str, Any]) -> "Struct":
        return cls(**value)

    @classmethod
    def pack(cls, value: "Struct") -> Dict[Any, Any]:
        assert isinstance(value, cls)
        return {name: field.pack(getattr(value, name)) for name, field in value.fields.items() if hasattr(value, name)}

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema.Object]) -> "Struct":
        if "ref" in document:
            return schemas[document["ref"]]
        return type(document["name"], (cls,), {
            "fields": {name: Schema.make(field, schemas) for name, field in document["fields"].items()},
            "schemas": {}
        })

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, ", ".join(["%s=%r" % (field, getattr(self, field, None)) for field in self.fields.keys()]))

Schema.register(Struct)

class Object(Struct, Schema.NonObject):
    name = "object"

    @classmethod
    def new(cls, name: str, fields: Dict[str, Any]) -> "Object":
        return type(name, (cls,), {"__annotations__": fields})

    @classmethod
    def pack(cls, value):
        return super().pack(cls(**value))

    @classmethod
    def dump(cls) -> Dict[str, Any]:
        return super().format()

Schema.register(Object)

class Field:

    class Base(Schema.Base, metaclass = Schema.Meta):
        type: Type

        @classmethod
        def create(cls, value: Any) -> Any:
            assert isinstance(value, cls.type)
            return value

        @classmethod
        def pack(cls, value: Any) -> Any:
            assert isinstance(value, cls.type)
            return value

        @classmethod
        def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema.Object]) -> "Field":
            return cls

    @staticmethod
    def register(field: "Field.Base"):
        Schema.Map.update({
            field.name: field,
            field.type: field
        })

class String(Field.Base):
    name = "string"
    type = str

Field.register(String)

class Base64(Field.Base):
    name = "base64"
    type = bytes

    @classmethod
    def create(cls, value: str) -> bytes:
        return base64.b64decode(value.encode())

    @classmethod
    def pack(cls, value: bytes) -> str:
        return base64.b64encode(value).decode()

Field.register(Base64)

class Integer(Field.Base):
    name = "integer"
    type = int

Field.register(Integer)

class Double(Field.Base):
    name = "Double"
    type = float

Field.register(Double)

class Boolean(Field.Base):
    name = "boolean"
    type = bool

Field.register(Boolean)

class Array(Field.Base):
    name = "array"
    type = list

    item: Schema.Base

    def __init__(self, item: Schema.Base) -> None:
        self.item = Schema.select(item, self.schemas)

    def dump(self):
        return {
            "type": self.name,
            "item": self.item.dump(),
        }

    def create(self, value: List[Any]) -> List[Any]:
        return [self.item.create(item) for item in value]

    def pack(self, value: List[Any]) -> List[Any]:
        return [self.item.pack(item) for item in value]

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema.Object]) -> "Array":
        return cls(Schema.make(document["item"], schemas))

Field.register(Array)

class Map(Field.Base):
    name = "map"
    type = list

    key: Schema.Base
    value: Schema.Base

    def __init__(self, key: Schema.Base, value: Schema.Base) -> None:
        self.key = Schema.select(key, self.schemas)
        self.value = Schema.select(value, self.schemas)

    def dump(self):
        return {
            "type": self.name,
            "key": self.key.dump(),
            "value": self.value.dump()
        }

    def create(self, value: Dict[Any, Any]) -> Dict[Any, Any]:
        return {self.key.create(key): self.value.create(value) for key, value in value.items()}

    def pack(self, value: Dict[Any, Any]) -> Dict[Any, Any]:
        return {self.key.pack(key): self.value.pack(value) for key, value in value.items()}

    @classmethod
    def make(cls, document: Dict[str, Any], schemas: Dict[str, Schema.Object]) -> "Map":
        return cls(Schema.make(document["key"], schemas), Schema.make(document["value"], schemas))

Field.register(Map)

class ANY(Field.Base):
    name = "any"
    type = None

    @classmethod
    def create(cls, value: Any) -> Any:
        return value

    @classmethod
    def pack(cls, value: Any) -> Any:
        return value

Field.register(ANY)