import threading
import collections

class ContextStack(object):
    __slots__ = ["_local", "base"]

    class StackUnderflow(Exception):
        pass

    def __init__(self):
        super(ContextStack, self).__init__()

        object.__setattr__(self, "base", Context())
        object.__setattr__(self, "_local", threading.local())
        self._local.stack = [Context(self.base)]

    @property
    def _heap(self):
        if self._local.stack:
            return self._local.stack[-1]

        else:
            return self.base

    def __iter__(self):
        yield self.base
        for c in self._local.stack:
            yield c

    def __getattr__(self, attr):
        return getattr(self._heap, attr)

    def __setattr__(self, attr, value):
        return setattr(self._heap, attr, value)

    def __delattr__(self, attr):
        return delattr(self._heap, attr)

    def push(self):
        new_context = Context(self._heap)
        self._local.stack.append(new_context)
        return new_context

    def pop(self):
        if len(self._local.stack) == 1:
            raise self.StackUnderflow()

        self._local.stack.pop(-1)

    def __enter__(self):
        return self.push()

    def __exit__(self, *exc):
        self.pop()

    def __dir__(self):
        r = set()
        for c in self:
            r.update(c._dict)
        return list(r)

    def __getitem__(self, index):
        assert index <= 0
        return self._local.stack[index - 1]

    def __len__(self):
        return len(self._local.stack)

class Context(object):
    __slots__ = ["_parent", "_dict"]

    def __init__(self, parent = None):
        assert parent == None or isinstance(parent, Context)

        super(Context, self).__init__()

        object.__setattr__(self, "_parent", parent)
        object.__setattr__(self, "_dict", {})

    @property
    def _parents(self):
        o = self
        while o:
            yield o 
            o = o._parent

    def __getattr__(self, attr):
        for c in self._parents:
            if attr in c._dict:
                return c._dict[attr]

        raise AttributeError(attr)

    def __delattr__(self, attr):
        del self._dict[attr]

    def __setattr__(self, attr, value):
        self._dict[attr] = value

    def __dir__(self):
        r = set()
        for c in self._parents:
            r.update(c._dict)
        return list(r)

