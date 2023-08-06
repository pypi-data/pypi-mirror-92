from .resources import Http, Client, create
import json

DISCOVERY_URI = "http://api.lesting.dev/discovery/v1/services/{service}/{version}/rest"

def build(service: str, version: int) -> Client:
    http = Http()
    headers, response = http.request(DISCOVERY_URI.format_map({
        "service": service,
        "version": version
    }))
    assert headers["status"] == "200"
    return create(json.loads(response), http)