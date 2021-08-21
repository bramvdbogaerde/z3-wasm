
from dataclasses import dataclass
from typing import Any

@dataclass
class DispatchItem:
    kind: Any
    method: Any

    def __call__(self, *args, **kwargs): 
        return self.method(*args, **kwargs)
    
    


def visitor(on):
    """
    Decorates a class and declares it as a visitor should that certain methods can be invoked on particular typs of nodes
    """
    def accept(self, item): 
        if on(item) in self.__visitor_dispatcher:
            return self.__visitor_dispatcher[on(item)](self, item)
        else:
            return item

    def inner(cls): 
        dispatcher = {}
        for _, method in cls.__dict__.items():
            if isinstance(method, DispatchItem):
                dispatcher[method.kind] = method

        cls.__visitor_dispatcher = dispatcher
        cls.accept = accept

        return cls

    return inner


def visit(tpy):
    def inner(func):
        return DispatchItem(tpy, func)

    return inner

def get_next(iterator):
    try: 
        return next(iterator)
    except StopIteration:
        return None

