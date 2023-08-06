X(), for low level debugging.

*Latest release 20210123*:
X: honour new $CS_X_COLOUR environment variable setting the default colour, default uncoloured.

X() is my function for low level ad hoc debug messages.
It takes a message and optional format arguments for use with `%`.
It is presented here in its own module for reuse:

    from cs.x import X
    ...
    X("foo: x=%s, a=%r", x, a)

It normally writes directly to `sys.stderr` but accepts an optional
keyword argument `file` to specify a different filelike object.

The following globals are further tune its behaviour,
absent the `file=` parameter:
* `X_logger`: if not `None` then log a warning to that logger
* `X_via_tty`: if true then open `/dev/tty` and write the message to it
* `X_discard`: if true then discard the message
Otherwise write the message to `sys.stderr`.

`X_via_tty` defaults to true if the environment variable `$CS_X_VIA_TTY`
has a nonempty value, false otherwise.
This is handy for getting debugging out of test suites,
which often divert `sys.stderr`.

`X_discard`'s default value is `not sys.stderr.isatty()`.

## Function `X(msg, *args, **kw)`

Unconditionally write the message `msg`.

If there are positional arguments after `msg`,
format `msg` using %-expansion with those arguments.

Keyword arguments:
* `file`: optional keyword argument specifying the output file.
* `colour`: optional text colour.
  If specified, surround the message with ANSI escape sequences
  to render the text in that colour.

If `file` is not `None`, write to it unconditionally.
Otherwise, the following globals are consulted in order:
* `X_logger`: if not `None` then log a warning to that logger
* `X_via_tty`: if true then open `/dev/tty` and write the message to it
* `X_discard`: if true then discard the message
Otherwise write the message to `sys.stderr`.

`X_logger` is `None` by default.
`X_via_tty` is true if the environment variable `$CS_X_VIA_TTY` is not empty,
false otherwise.
`X_discard` is true unless `sys.stderr.isatty()` is true.

## Function `Xtty(msg, *args, **kw)`

Call `X()` with `X_via_tty` set to `True`.

*Note*:
this is now obsoleted by the `$CS_X_VIA_TTY` environment variable.

This supports using:

    from cs.x import Xtty as X

when hacking on tests without the tedious shuffle:

    from cs.x import X
    import cs.x; cs.x.X_via_tty = True

which I did _a lot_ to get timely debugging when fixing test failures.

## Function `Y(msg, *a, **kw)`

Wrapper for `X()` rendering in yellow.

# Release Log



*Release 20210123*:
X: honour new $CS_X_COLOUR environment variable setting the default colour, default uncoloured.

*Release 20201227*:
New Y() which calls X(...,colour=yellow) - I now often go `from cs.x import Y as X`.

*Release 20201102*:
* Set X_via_tty if $CS_X_VIA_TTY.
* Put X() into builtins if $CS_X_BUILTIN.

*Release 20181231*:
* X: trivial ANSI colour support via new `colour` keyword argument.
* New global X_discard, False unless sys.stderr.isatty.

*Release 20180726*:
doco improvements

*Release 20170902*:
Move X() into its own module, used for ad hoc debugging everywhere.

*Release 20170707.3*:
tweak DISTINFO

*Release 20170707.2*:
Doc tweak.

*Release 20170707.1*:
Added README.

*Release 20170707*:
Separate X() out into new module cs.x for cheap import.
