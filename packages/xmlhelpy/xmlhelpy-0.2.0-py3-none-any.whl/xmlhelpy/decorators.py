# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import keyword
import string

import click

from .core import Argument
from .core import Command
from .core import Group
from .core import Option
from .formatting import print_commands
from .formatting import print_version
from .formatting import print_xmlhelp


def group(name=None, version=None):
    """Decorator to register a new command group.

    Group names will be listed before the actual command name in the generated xmlhelp.

    :param name: (optional) The name of the command. Defaults to the name of the
        decorated function with underscores replaced by dashes.
    :param version: (optional) The version of the group as string. This version will be
        inherited by all commands and subgroups of this group that do not explicitely
        specify their own version.
    """

    def decorator(func):
        click.option(
            "--commands",
            help="Print a list of all commands this group contains.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_commands,
        )(func)

        click.option(
            "--version",
            help="Print the version of this group and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_version,
        )(func)

        return click.group(cls=Group, name=name, version=version)(func)

    return decorator


def command(name=None, description=None, example="", version=None):
    """Decorator to register a new command or underlying tool.

    :param name: (optional) The name of the command. Defaults to the name of the
        decorated function with underscores replaced by dashes.
    :param description: (optional) The description of the command. Defaults to the
        docstring of the decorated function.
    :param example: (optional) An example of using the command.
    :param version: (optional) The version of the command as string.
    """

    def decorator(func):
        click.option(
            "--xmlhelp",
            help="Print the XML help and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_xmlhelp,
        )(func)

        click.option(
            "--version",
            help="Print the version of this command and exit.",
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=print_version,
        )(func)

        cmd = click.command(
            cls=Command,
            name=name,
            version=version,
            example=example,
            description=description,
        )(func)

        return cmd

    return decorator


def argument(
    name,
    description="",
    nargs=1,
    param_type=None,
    required=True,
    default=None,
    as_string=False,
):
    """Decorator to add an argument parameter to a command.

    Arguments are positional parameters with less possibilities than options that are
    also required by default.

    :param name: The name of the argument.
    :param description: (optional) The description of the argument.
    :param nargs: (optional) The number of arguments (separated by spaces) to expect.
        ``-1`` can be specified to allow for an unlimited number of arguments.
    :param param_type: (optional) The type of the argument parameter, either as class or
        instance. See :mod:`xmlhelpy.types` for the possible parameter types.
    :param required: (optional) Flag indicating wether the argument is required or not.
    :param default: (optional) The default value to take if the argument is not given.
    :param as_string: (optional) If ``True`` the argument will be converted to a string
        before passing it to the command function. This should make it easier to pass on
        any values to an external command without needing to convert them first. For
        values that are normally passed in as ``None``, an empty string will be used
        instead.
    """

    def decorator(func):
        click.argument(
            name,
            cls=Argument,
            description=description,
            nargs=nargs,
            param_type=param_type,
            as_string=as_string,
            required=required,
            default=default,
        )(func)

        return func

    return decorator


def option(
    name,
    description="",
    nargs=1,
    param_type=None,
    required=False,
    default=None,
    as_string=False,
    char=None,
    var_name=None,
    is_flag=False,
):
    """Decorator to add an option parameter to a command.

    Options are non-positional parameters or flags.

    :param name: The full name of the option, which has to be given as
        ``--<name> <value>`` when invoking the command.
    :param description: (optional) The description of the option.
    :param nargs: (optional) The number of arguments (separated by spaces) to expect.
        ``-1`` can be specified to allow for an unlimited number of arguments.
    :param param_type: (optional) The type of the option parameter, either as class or
        instance. See :mod:`xmlhelpy.types` for the possible parameter types.
    :param required: (optional) Flag indicating wether the option is required or not.
    :param default: (optional) The default value to take if the option is not given.
    :param as_string: (optional) If ``True`` the parameter will be converted to a string
        before passing it to the command function. This should make it easier to pass on
        any values to an external command without needing to convert them first. Only
        flags and ``None`` values will be passed in as is.
    :param char: (optional) A shorthand for an option consisting of a single ASCII
        letter, which has to be given as ``-<char> <value>`` when invoking the command.
    :param var_name: (optional) The name of the variable that will be passed into the
        executing function. Defaults to the name in lowercase, with dashes replaced by
        underscores.
    :param is_flag: (optional) Flag indicating wether the option is a flag. Flags are
        special options that do not require a value. They always use :class:`.Bool` as
        type and always use ``False`` as default value. Flags always return boolean
        values, even if ``as_string`` is given.
    """

    def decorator(func):
        # It is best to deal with the parameter names here already before passing them
        # to the original option decorator.
        if "/" in name:
            raise click.BadOptionUsage(name, "Name cannot contain slashes.")

        if char is not None and char not in string.ascii_letters:
            raise click.BadOptionUsage(name, "Invalid char value.")

        if var_name is not None and (
            keyword.iskeyword(var_name) or not var_name.isidentifier()
        ):
            raise click.BadOptionUsage(name, "Invalid variable name.")

        param_decls = ["--" + name]

        if char is not None:
            param_decls.append("-" + char)

        if var_name is not None:
            param_decls.append(var_name)

        click.option(
            *param_decls,
            cls=Option,
            description=description,
            nargs=nargs,
            param_type=param_type,
            as_string=as_string,
            required=required,
            default=default,
            char=char,
            is_flag=is_flag,
            show_default=True,
        )(func)

        return func

    return decorator
