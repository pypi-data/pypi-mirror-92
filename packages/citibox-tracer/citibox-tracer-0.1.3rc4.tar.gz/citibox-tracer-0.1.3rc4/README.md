# tracing-library
[Opencensus](https://opencensus.io/) python wrapper for traceability

## Usage

### How to enable
the tracing require environment variable to start
```python
TRACER = True
```
### Falcon Middleware

Enable the middleware in your app.

```python
import falcon
from citibox.google_cloud_tracer.contrib.falcon import GoogleCloudFalconMiddleware
from opencensus.trace import samplers

googleCloudTracer = GoogleCloudFalconMiddleware(
    "your-project", 
    ["/", "/health", "/another-not-traceable"],
    samplers.AlwaysOnSampler()
)

app = falcon.API(middleware=[googleCloudTracer])
```

### Requests wrapper
There is a `requests` wrapper to make http requests traceables

````python
from citibox.google_cloud_tracer import requests

r_get = requests.get('https://google.com', {"param": "something"})

r_post = requests.post('https://google.com', json={"something": "value"})
````

You can use `requests` wrapper as native `requests` library.

> requests.Session() not applied, you will need to get the trace headers if you are using sessions 
### Django Middleware

Enable the middleware in your app.

```python
MIDDLEWARE = [
    ...,
    'citibox.google_cloud_tracer.contrib.django.GoogleCloudDjangoMiddleware',
    ...,
]

TRACING = {
    'PROJECT_ID': 'your-project-id',
    'EXCLUDELIST_HOSTNAMES': ['localhost', '127.0.0.1'],
    'EXCLUDELIST_PATHS': ['_ah/health'],
}
```