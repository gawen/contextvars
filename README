# contextvars

``contextvars`` is a Python module to manage contexted variables.

## Examples

    from contextvars import *

    c = ContextStack()

    c.foo = "foo"
    with c:
        assert c.foo == "foo"

        c.foo = "bar"

        assert c.foo == "bar"

    assert c.foo == "foo"
