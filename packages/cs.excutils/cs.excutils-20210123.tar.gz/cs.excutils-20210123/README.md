Convenience facilities for managing exceptions.

*Latest release 20210123*:
@transmute: refactor to raise chained exceptions in Python 3+.

## Function `exc_fold(*da, **dkw)`

Decorator to catch specific exception types and return a defined default value.

## Function `logexc(func)`

Decorator to log exceptions and reraise.

## Function `logexc_gen(genfunc)`

Decorator to log exceptions and reraise for generators.

## Function `LogExceptions(conceal=False)`

Wrapper for `NoExceptions` which reports exceptions and optionally
suppresses them.

## Function `noexc(func)`

Decorator to wrap a function which should never raise an exception.
Instead, any raised exception is attempted to be logged.

A significant side effect is of course that if the function raises an
exception it now returns `None`.
My primary use case is actually to wrap logging functions,
which I have had abort otherwise sensible code.

## Function `noexc_gen(func)`

Decorator to wrap a generator which should never raise an exception.
Instead, any raised exception is attempted to be logged and iteration ends.

My primary use case is wrapping generators chained in a pipeline,
as in cs.later.Later.pipeline.

## Class `NoExceptions`

A context manager to catch _all_ exceptions and log them.

Arguably this should be a bare try...except but that's syntacticly
noisy and separates the catch from the top.
For simple function calls `return_exc_info()` is probably better.

### Method `NoExceptions.__init__(self, handler)`

Initialise the `NoExceptions` context manager.

The `handler` is a callable which
expects `(exc_type,exc_value,traceback)`
and returns `True` or `False`
for the `__exit__` method of the manager.
If `handler` is `None`, the `__exit__` method
always returns `True`, suppressing any exception.

## Function `return_exc_info(func, *args, **kwargs)`

Run the supplied function and arguments.
Return `(func_return, None)`
in the case of successful operation
and `(None, exc_info)` in the case of an exception.

`exc_info` is a 3-tuple of `(exc_type, exc_value, exc_traceback)`
as returned by `sys.exc_info()`.
If you need to protect a whole suite and would rather not move it
into its own function, consider the NoExceptions context manager.

## Function `returns_exc_info(func)`

Decorator function to wrap functions whose exceptions should be caught,
such as inside event loops or worker threads.

It causes a function to return `(func_return, None)`
in the case of successful operation
and `(None, exc_info)` in the case of an exception.

`exc_info` is a 3-tuple of `(exc_type, exc_value, exc_traceback)`
as returned by `sys.exc_info()`.

## Function `safe_property(func)`

Substitute for @property which lets AttributeErrors escape as RuntimeErrors.

## Function `transmute(*da, **dkw)`

Decorator to transmute an inner exception to another exception type.

The motivating use case is properties in a class with a
`__getattr__` method;
if some inner operation of the property function raises `AttributeError`
then the property is bypassed in favour of `__getattr__`.
Confusion ensues.

In principle this can be an issue with any exception raised
from "deeper" in the call chain, which can be mistaken for a
"shallow" exception raised by the function itself.

## Function `unattributable(func)`

Decorator to transmute `AttributeError` into a `RuntimeError`.

## Function `unimplemented(func)`

Decorator for stub methods that must be implemented by a stub class.

# Release Log



*Release 20210123*:
@transmute: refactor to raise chained exceptions in Python 3+.

*Release 20190812*:
LogExceptions: drop stack trace noise.

*Release 20190220*:
New decorator @exc_fold to catch particular exceptions, log an error and return a defined value.

*Release 20190101*:
@logexc: handle missing func.__name__.

*Release 20170904*:
Minor updates, improved docstring.

*Release 20160828*:
* @unattributable and @safe_property decorators, used to protect properties from inner AttributeErrors.
* Improved exception practices.

*Release 20150118*:
metadata updates

*Release 20150110*:
Initial distinfo for pypi release.
