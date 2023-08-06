# tracing-library
[Opencensus](https://opencensus.io/) python wrapper for traceability

## Usage
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
