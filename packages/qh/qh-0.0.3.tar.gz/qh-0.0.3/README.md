
# qh
Quick Http web-service construction.

Getting from python to an http-service exposing them to the world, 
in the easiest way machinely possible.

Harnesses the great power of [py2http](https://github.com/i2mint/py2http) 
without all the responsibilities. 

This is meant for the desireable lightening fast development cycles during 
proof-of-conceptualization. 
As you move towards production, consider using one of those boring grown-up tools out there... 


To install:	```pip install qh```

# Examples

## When dealing only with simple (json) types...

```python
import qh
from qh import mk_http_service_app

def poke():
    return 'here is a peek'

def foo(x: int):
    return x + 2

def bar(name='world'):
    return f"Hello {name}!"

app = mk_http_service_app([foo, bar, poke])
app.run()
```

```
Bottle v0.12.19 server starting up (using WSGIRefServer())...
Listening on http://127.0.0.1:8080/
Hit Ctrl-C to quit.
```

Now grab a browser and go to `http://127.0.0.1:8080/ping` 
(it's a GET route that the app gives you for free, to test if alive)

```
{"ping": "pong"}
```

Now try some post requests:

Run this script somewhere. For example, with curl try things like:

```
curl http://127.0.0.1:8080/ping
# should get {"ping": "pong"}

curl -X POST http://127.0.0.1:8080/poke
# should get "here is a peek"

curl -H "Content-Type: application/json" -X POST -d '{"x": 3}' http://127.0.0.1:8080/foo
# (should get 5)

curl -H "Content-Type: application/json" -X POST -d '{"name": "qh"}' http://127.0.0.1:8080/bar
# should get "hello qh!"
```

Now be happy (or go try the other function by doing some post requests).

## When your types get complicated

To deploy the above, we would just need to do 
```python
app = mk_http_service_app([poke, foo, bar])
```

But what if we also wanted to handle this:

```python
def add_numpy_arrays(a, b):
    return (a + b).tolist()
```


Here the a and b are assumed to be numpy arrays (or .tolist() would fail).
Out of the box, qh can only handle json types (str, list, int, float), so we need to preprocess the input. 
`qh` makes that easy too. 

Here we provide a name->conversion_func mapping (but could express it otherwise)

```python
from qh.trans import mk_json_handler_from_name_mapping
import numpy as np

input_trans = mk_json_handler_from_name_mapping(
    {
        "a": np.array,
        "b": np.array
    }
)

app = mk_http_service_app([poke, foo, bar, add_numpy_arrays],
                          input_trans=input_trans)
```
