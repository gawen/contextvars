import nose
from contextvars import *
import threading

import contextlib
@contextlib.contextmanager
def assert_exception(exc):
    try:
        yield

    except exc, e:
        return

    else:
        raise AssertionError("No exception had been raised.")

def test_simplepushpop():
    c = ContextStack()

    c.a = 42
    assert c.a == 42

    c.push()
    assert c.a == 42
    c.a = 24
    assert c.a == 24
    c.pop()

    assert c.a == 42

def test_simplecontext():
    c = ContextStack()

    c.a = 42
    assert c.a == 42

    with c:
        assert c.a == 42

        c.a = 24
        assert c.a == 24

    assert c.a == 42

def test_del():
    c = ContextStack()

    c.a = 42
    assert c.a == 42

    del c.a

    with assert_exception(AttributeError):
        c.a

def test_del_push():
    c = ContextStack()

    c.a = 42
    assert c.a == 42

    with c:
        assert c.a == 42

        c.a = 24
        assert c.a == 24

        del c.a
        assert c.a == 42

    assert c.a == 42

def test_underflow():
    c = ContextStack()

    with assert_exception(ContextStack.StackUnderflow):
        c.pop()

def test_dir():
    c = ContextStack()

    c.a = 42

    assert "a" in dir(c)

    with c:
        assert "a" in dir(c)

    assert "a" in dir(c)

    del c.a
    assert "a" not in dir(c)

def test_len():
    c = ContextStack()
    
    assert len(c) == 1
    with c:
        assert len(c) == 2
        with c:
            assert len(c) == 3
        assert len(c) == 2
    assert len(c) == 1

def test_inherit():
    c = ContextStack()

    c.a = 42
    assert c.a == 42

    with c:
        assert c.a == 42

        c[-1].a = "foo"
        assert c.a == "foo"

        c.a = 24
        assert c.a == 24
        assert c[-1].a == "foo"

        del c.a
        assert c.a == "foo"

    assert c.a == "foo"

def test_base():
    c = ContextStack()

    c.base.a = 42

    assert c.base.a == 42
    assert c.a == 42

    c.a = 24
    assert c.a == 24

    del c.a
    assert c.a == 42

