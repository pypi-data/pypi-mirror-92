__all__ = [
    "Method",
    "Resource",
    "Service",
    "Client",
]

from typing import Callable, Union, Tuple, Dict, List, Any
from .schemas import Schema
from itertools import zip_longest
from httplib2 import Http
import json
import re

class Method:

    base: "Resource"
    func: Callable

    def __init__(self, base: "Resource", func: Callable, method: str, parameters: Dict[str, Schema.Base], response: Schema.Base) -> None:
        self.base = base
        self.func = func
        self.name = func.__name__
        self.method = method
        self.path = base.path + [self.name]
        self.parameters = parameters
        self.response = response

    def __call__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Any:
        return self.func(*args, **kwargs)

    def dump(self):
        return {
            "type": "method",
            "name": self.name,
            "method": self.method,
            "path": "/".join(self.path),
            "parameters": {name: parameter.dump() for name, parameter in self.parameters.items()},
            "response": self.response.dump()
        }

class Resource:

    resources: Dict[str, "Resource"]
    schemas: Dict[str, Schema.Object]

    def __init__(self, base: "Resource", name: str) -> None:
        self.base = base
        self.name = name
        self.resources = {}

    def __getattr__(self, name: str):
        return self.resources.get(name)

    @property
    def schemas(self) -> Dict[str, Schema.Base]:
        return self.base.schemas

    @property
    def path(self) -> List[str]:
        return self.base.path + [self.name]

    def dump(self):
        return {
            "type": "resource",
            "name": self.name,
            "resources": {name: resource.dump() for name, resource in self.resources.items()}
        }

class Service(Resource):

    name: str
    version: int
    base: str
    path: List[str] = None
    schemas: Dict[str, Schema.Object] = None

    def __init__(self, name: str, version: int, base: str = None) -> None:
        self.name = name
        self.version = version
        self.base = base
        self.path = ["", self.name, self.version]
        self.resources = {}
        self.schemas = {}

    def dump(self):
        return {
            "type": "service",
            "name": self.name,
            "version": self.version,
            "base": self.base,
            "schemas": {name: schema.format() for name, schema in self.schemas.items()},
            "resources": {name: resource.dump() for name, resource in self.resources.items()}
        }

class Client:

    def __init__(self, service: Service, http: Http) -> None:
        self.service = service
        self.http = http
        self.headers = {
            "Content-Type": "application/json"
        }

    @property
    def schemas(self):
        return self.service.schemas

    def request(self, method: str, path: str, parameters: Dict[str, Schema]):
        headers, response = self.http.request(self.service.base + path, method, json.dumps(parameters), self.headers)
        assert headers["status"] == "200"
        return json.loads(response)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.service, name)

REGEX = re.compile(r"({[a-zA-Z0-9.]+})")

def create(document: Dict[str, Any], base: Union[Client, Http] = None):

    if document["type"] == "service":
        service = Service(document["name"], document["version"], document["base"])
        client = Client(service, base)
        for name, value in document["schemas"].items():
            service.schemas[name] = Schema.make(value, service.schemas)
        for name, value in document["resources"].items():
            service.resources[name] = create(value, client)
        return client

    elif document["type"] == "resource":
        resource = Resource(base, document["name"])
        for name, value in document["resources"].items():
            resource.resources[name] = create(value, base)
        return resource

    elif document["type"] == "method":
        parameters = {name: Schema.make(parameter, base.schemas) for name, parameter in document["parameters"].items()}
        response = Schema.make(document["response"], base.schemas)
        groups = [match.group()[1:-1] for match in REGEX.finditer(document["path"])]
        def func(*args: Any, **kwargs: Any) -> Any:
            for parameter, value in zip_longest(parameters.items(), args):
                if value is not None:
                    kwargs[parameter[0]] = value
                if getattr(parameter[1], "required", True) and parameter[0] not in kwargs:
                    raise TypeError("`%s` required" % (parameter[0]))
            path = document["path"].format_map({name: kwargs[name] for name in groups})
            return response.create(base.request(document["method"], path, {name: parameters[name].pack(value) for name, value in kwargs.items()}))
        method = Method(base, func, document["method"], parameters, response)
        method.func = func
        method.path = document["path"].split("/")
        method.parameters = parameters
        method.response = response
        return method