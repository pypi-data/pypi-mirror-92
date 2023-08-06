Convenience functions for working with the Cmd module
and other command line related stuff.

*Latest release 20210123*:
BaseCommand: propagate the format mapping (cmd, USAGE_KEYWORDS) to the subusage generation.

## Class `BaseCommand`

A base class for handling nestable command lines.

This class provides the basic parse and dispatch mechanisms
for command lines.
To implement a command line
one instantiates a subclass of BaseCommand:

    class MyCommand(BaseCommand):
      GETOPT_SPEC = 'ab:c'
      USAGE_FORMAT = r"""Usage: {cmd} [-a] [-b bvalue] [-c] [--] arguments...
        -a    Do it all.
        -b    But using bvalue.
        -c    The 'c' option!
      """
    ...
    the_cmd = MyCommand()

Running a command is done by:

    the_cmd.run(argv)

The subclass is customised by overriding the following methods:
* `apply_defaults(options)`:
  prepare the initial state of `options`
  before any command line options are applied
* `apply_opts(options,opts)`:
  apply the `opts` to `options`.
  `opts` is an `(option,value)` sequence
  as returned by `getopot.getopt`.
* `cmd_`*subcmd*`(argv,options)`:
  if the command line options are followed by an argument
  whose value is *subcmd*,
  then the method `cmd_`*subcmd*`(argv,options)`
  will be called where `argv` contains the command line arguments
  after *subcmd*.
* `main(argv,options)`:
  if there are no command line aguments after the options
  or the first argument does not have a corresponding
  `cmd_`*subcmd* method
  then method `main(argv,options)`
  will be called where `argv` contains the command line arguments.
* `run_context(argv,options,cmd)`:
  a context manager to provide setup or teardown actions
  to occur before and after the command implementation respectively.
  If the implementation is a `cmd_`*subcmd* method
  then this is called with `cmd=`*subcmd*;
  if the implementation is `main`
  then this is called with `cmd=None`.

To aid recursive use
it is intended that all the per command state
is contained in the `options` object
and therefore that in typical use
all of `apply_opts`, `cmd_`*subcmd*, `main` and `run_context`
should be static methods making no reference to `self`.

Editorial: why not arparse?
Primarily because when incorrectly invoked
an argparse command line prints the help/usage messgae
and aborts the whole programme with `SystemExit`.

### `BaseCommand.OPTIONS_CLASS`

SKIP DOC: A simple attribute-based namespace.

SimpleNamespace(**kwargs)

### Method `BaseCommand.add_usage_to_docstring()`

Append `cls.usage_text()` to `cls.__doc__`.

### Method `BaseCommand.apply_defaults(self, options)`

Stub `apply_defaults` method.

Subclasses can override this to set up the initial state of `options`.

### Method `BaseCommand.cmd_help(argv, options)`

Usage: {cmd} [subcommand-names...]
Print the help for the named subcommands,
or for all subcommands if no names are specified.

### Method `BaseCommand.getopt_error_handler(cmd, options, e, usage)`

The `getopt_error_handler` method
is used to control the handling of `GetoptError`s raised
during the command line parse
or during the `main` or `cmd_`*subcmd*` calls.

The handler is called with these parameters:
* `cmd`: the command name
* `options`: the `options` object
* `e`: the `GetoptError` exception
* `usage`: the command usage or `None` if this was not provided

It returns a true value if the exception is considered handled,
in which case the main `run` method returns 2.
It returns a false value if the exception is considered unhandled,
in which case the main `run` method reraises the `GetoptError`.

This default handler prints an error message to standard error,
prints the usage message (if specified) to standard error,
and returns `True` to indicate that the error has been handled.

To let the exceptions out unhandled
this can be overridden with a method which just returns `False`
or even by setting the `getopt_error_handler` attribute to `None`.

Otherwise,
the handler may perform any suitable action
and return `True` to contain the exception
or `False` to cause the exception to be reraised.

### Method `BaseCommand.run(self, argv=None, options=None, cmd=None)`

Run a command from `argv`.
Returns the exit status of the command.
Raises `GetoptError` for unrecognised options.

Parameters:
* `argv`:
  optional command line arguments
  including the main command name if `cmd` is not specified.
  The default is `sys.argv`.
  The contents of `argv` are copied,
  permitting desctructive parsing of `argv`.
* `options`:
  a object for command state and context.
  If not specified a new `SimpleNamespace`
  is allocated for use as `options`,
  and prefilled with `.cmd` set to `cmd`
  and other values as set by `.apply_defaults(options)`
  if such a method is provided.
* `cmd`:
  optional command name for context;
  if this is not specified it is taken from `argv.pop(0)`.

The command line arguments are parsed according to `getopt_spec`.
If `getopt_spec` is not empty
then `apply_opts(opts,options)` is called
to apply the supplied options to the state
where `opts` is the return from `getopt.getopt(argv,getopt_spec)`.

After the option parse,
if the first command line argument *foo*
has a corresponding method `cmd_`*foo*
then that argument is removed from the start of `argv`
and `self.cmd_`*foo*`(argv,options,cmd=`*foo*`)` is called
and its value returned.
Otherwise `self.main(argv,options)` is called
and its value returned.

If the command implementation requires some setup or teardown
then this may be provided by the `run_context`
context manager method,
called with `cmd=`*subcmd* for subcommands
and with `cmd=None` for `main`.

### Method `BaseCommand.run_context(argv, options)`

Stub context manager which surrounds `main` or `cmd_`*subcmd*.

### Method `BaseCommand.subcommand_usage_text(subcmd, fulldoc=False, usage_format_mapping=None)`

Return the usage text for a subcommand.

Parameters:
* `subcmd`: the subcommand name
* `fulldoc`: if true (default `False`)
  return the full docstring with the Usage section expanded
  otherwise just return the Usage section.

### Method `BaseCommand.subcommands()`

Return a mapping of subcommand names to class attributes
for attributes which commence with `cls.SUBCOMMAND_METHOD_PREFIX`
by default `'cmd_'`.

### Method `BaseCommand.usage_text(*a, **kw)`

Compute the "Usage: message for this class
from the top level `USAGE_FORMAT`
and the `'Usage:'`-containing docstrings
from its `cmd_*` methods.

This is a cached method because it tries to update the
method docstrings after formatting, which is bad if it
happens more than once.

## Function `docmd(dofunc)`

Decorator for `cmd.Cmd` subclass methods
to supply some basic quality of service.

This decorator:
- wraps the function call in a `cs.pfx.Pfx` for context
- intercepts `getopt.GetoptError`s, issues a `warning`
  and runs `self.do_help` with the method name,
  then returns `None`
- intercepts other `Exception`s,
  issues an `exception` log message
  and returns `None`

The intended use is to decorate `cmd.Cmd` `do_`* methods:

    from cmd import Cmd
    from cs.cmdutils import docmd
    ...
    class MyCmd(Cmd):
      @docmd
      def do_something(...):
        ... do something ...

# Release Log



*Release 20210123*:
BaseCommand: propagate the format mapping (cmd, USAGE_KEYWORDS) to the subusage generation.

*Release 20201102*:
* BaseCommand.cmd_help: supply usage only for "all commands", full docstring for specified commands.
* BaseCommand: honour presupplied options.log_level.
* BaseCommand.usage_text: handle missing USAGE_FORMAT better.
* BaseCommand.run: provide options.upd.
* BaseCommand subclasses may now override BaseCommand.OPTIONS_CLASS (default SimpleNamespace) in order to provide convenience methods on the options.
* BaseCommand.run: separate variable for subcmd with dash translated to underscore to match method names.
* Minor fixes.

*Release 20200615*:
BaseCommand.usage_text: do not mention the "help" command if it is the only subcommand (it won't be available if there are no other subcommands).

*Release 20200521.1*:
Fix DISTINFO.install_requires.

*Release 20200521*:
* BaseCommand.run: support using BaseCommand subclasses as cmd_* names to make it easy to nest BaseCommands.
* BaseCommand: new hack_postopts_argv method called after parsing the main command line options, for inferring subcommands or the like.
* BaseCommand: extract "Usage:" paragraphs from subcommand method docstrings to build the main usage message.
* BaseCommand: new cmd_help default command.
* Assorted bugfixes and small improvements.

*Release 20200318*:
* BaseCommand.run: make argv optional, get additional usage keywords from self.USAGE_KEYWORDS.
* @BaseCommand.add_usage_to_docstring: honour cls.USAGE_KEYWORDS.
* BaseCommand: do not require GETOPT_SPEC for commands with no defined options.
* BaseCommand.run: call cs.logutils.setup_logging.

*Release 20200229*:
Improve subcommand selection logic, replace StackableValues with stackattrs, drop `cmd` from arguments passed to main/cmd_* methods (present in `options`).

*Release 20200210*:
* New BaseCommand.add_usage_to_docstring class method to be called after class setup, to append the usage message to the class docstring.
* BaseCommand.run: remove spurious Pfx(cmd), as logutils does this for us already.

*Release 20190729*:
BaseCommand: support for a USAGE_FORMAT usage message format string and a getopt_error_handler method.

*Release 20190619.1*:
Another niggling docstring formatting fix.

*Release 20190619*:
Minor documentation updates.

*Release 20190617.2*:
Lint.

*Release 20190617.1*:
Initial release with @docmd decorator and alpha quality BaseCommand command line assistance class.
