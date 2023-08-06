from wrapt import decorator

from inspect import getfullargspec
from copy import deepcopy
from typing import Generator, Callable, Any

from .constants import ErrorMessages


class Extension:
    @staticmethod
    def extend(target_cls: "Extendable") -> None:
        """
        Any modification of the target class should take place in this function
        """

        raise NotImplementedError

    @staticmethod
    def can_extend(target_cls: "Extendable") -> bool:
        """
        Should return a bool indicating whether this Extension can be applied to the target class
        """

        raise NotImplementedError

    @staticmethod
    def wrap(target_cls: "Extendable", method_name: str,
             gen_func: Callable[["Extendable", Any, Any], Generator[None, Any, None]]) -> None:
        """
        Used to wrap an existing method on the target class.
        Passes copies of the method parameters to the generator function provided.
        The generator function should yield once,
        with the yield statement receiving a copy of the result of executing the core method
        """

        method = getattr(target_cls, method_name)
        method_args = getfullargspec(method).args

        if len(method_args) == 0 or method_args[0] != "self":
            ErrorMessages.wrap_static(method_name)

        @decorator  # This will preserve the original method signature when wrapping the method
        def wrapper(func, self, args, kwargs):
            gen = gen_func(self, *deepcopy(args), **deepcopy(kwargs))
            next(gen)

            result = func(*args, **kwargs)

            try:
                gen.send(deepcopy(result))
            except StopIteration:
                pass

            return result

        setattr(target_cls, method_name, wrapper(method))
