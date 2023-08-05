from inspect import iscoroutinefunction
from typing import Optional, Dict, Any

from wrapt import ObjectProxy

from veils._async_dummy import async_dummy
from veils.veil_factory import VeilFactory


class Unpiercable:
    __slots__ = (
        "_origin",
        "_methods",
        "_async_methods",
        "_props",
    )

    def __init__(
        self,
        wrapped,
        *,
        methods: Optional[Dict[str, Any]] = None,
        async_methods: Optional[Dict[str, Any]] = None,
        props: Optional[Dict[str, Any]] = None,
    ):
        self._origin = wrapped
        self._methods = {} if methods is None else methods
        self._async_methods = {} if async_methods is None else async_methods
        self._props = {} if props is None else props

    def __repr__(self):
        return "<{} at 0x{:x} for {} at 0x{:x}>".format(
            type(self).__name__, id(self), type(self._origin).__name__, id(self._origin)
        )

    def __getattribute__(self, attr):
        if attr == "__class__":
            return self._origin.__class__
        return object.__getattribute__(self, attr)

    def __getattr__(self, attr):
        if attr in self._props:
            return self._props[attr]
        method = getattr(self._origin, attr)
        if attr in self._methods:
            if iscoroutinefunction(method) or iscoroutinefunction(method.__call__):
                return CachedAsyncMethod(method, self._methods[attr])
            return CachedMethod(method, self._methods[attr])
        elif attr in self._async_methods:
            return CachedAsyncMethod(method, self._async_methods[attr])
        return method


class CachedMethod(ObjectProxy):
    def __init__(self, wrapped, cached: Any):
        super(CachedMethod, self).__init__(wrapped)
        self._self_cached: Any = cached

    def __call__(self, *args, **kwargs):
        return self._self_cached


class CachedAsyncMethod(ObjectProxy):
    def __init__(self, wrapped, cached_value: Any):
        super(CachedAsyncMethod, self).__init__(wrapped)
        self._self_cached: Any = cached_value

    def __call__(self, *args, **kwargs):
        return async_dummy(self._self_cached)


_default_factory = VeilFactory(Unpiercable)


def unpiercable(
    wrapped,
    *,
    methods: Optional[Dict[str, Any]] = None,
    async_methods: Optional[Dict[str, Any]] = None,
    props: Optional[Dict[str, Any]] = None,
):
    return _default_factory.veil_of(
        wrapped, methods=methods, async_methods=async_methods, props=props
    )
