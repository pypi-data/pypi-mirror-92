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
import click


class ParamTypeMixin:
    """Mixin that each parameter type should inherit from.

    Each parameter should at the very least have a ``name`` attribute.
    """

    name = "param"

    @property
    def xml_attrs(self):
        """Get the XML attributes of this parameter type.

        For use in the XML help of the arguments and options.

        :return: A dictionary representing the XML attributes.
        """
        return {
            "type": self.name,
        }

    @classmethod
    def to_string(cls, value):
        """Convert one or multiple values (as tuple) of this parameter type to a string.

        Values are simply converted to their default string representation. Multiple
        values (i.e. tuples) are afterwards combined with spaces inbetween. Spaces being
        part of the resulting string values will be escaped with a backslash.

        :param value: The value to convert.
        :return: The converted string value.
        """
        if isinstance(value, tuple):
            values = []
            for val in value:
                val = str(val).replace(" ", "\\ ")
                values.append(val)

            return " ".join(values)

        value = str(value).replace(" ", "\\ ")
        return value

    def convert(self, value, param, ctx):
        """Convert the parameter value.

        If the parameter should be represented as string, i.e. ``as_string`` is
        ``True``, :meth:`to_string` will be called to convert the value of the
        respective parameter type after the regular conversion is done. Only flags (in
        case of options) and ``None`` values will never be converted (as this method
        will not be called for ``None`` values).

        This is to be called only internally.
        """
        from .core import Option

        # If this method is called for a flag, we know it was given and should
        # be set to True.
        if isinstance(param, Option) and param.is_flag:
            return True

        result = super().convert(value, param, ctx)
        if param.as_string:
            return self.to_string(result)

        return result


class String(ParamTypeMixin, click.types.StringParamType):
    """String parameter type."""

    name = "string"

    def convert(self, value, param, ctx):
        """See :meth:`ParamTypeMixin.convert`.

        Ensures that the parameter value always gets converted to a string. Single
        quotes being part of a string value will be escaped with a backslash.
        """
        return str(super().convert(value, param, ctx))


class Bool(ParamTypeMixin, click.types.BoolParamType):
    """Boolean parameter type."""

    name = "bool"

    @staticmethod
    def _bool_to_string(value):
        if value is True:
            return "true"

        return "false"

    @classmethod
    def to_string(cls, value):
        """See :meth:`ParamTypeMixin.to_string`.

        ``True`` will be converted to ``'true'``, ``False`` to ``'false'``.
        """
        if isinstance(value, tuple):
            values = []
            for val in value:
                values.append(cls._bool_to_string(val))

            return " ".join(values)

        return cls._bool_to_string(value)


class Float(ParamTypeMixin, click.types.FloatParamType):
    """Float parameter type."""

    # name = 'float'
    name = "real"  # Compatibility with the current xmlhelp interface.


class FloatRange(ParamTypeMixin, click.types.FloatRange):
    """Float range parameter type.

    :param min: (optional) The minimum allowed float value.
    :param max: (optional) The maximum allowed float value.
    """

    name = "float_range"

    def __init__(self, min=None, max=None):
        min = float(min) if min is not None else min
        max = float(max) if max is not None else max
        super().__init__(min=min, max=max)

    @property
    def xml_attrs(self):
        """See :meth:`ParamTypeMixin.xml_attrs`.

        Includes the minimum and maximum allowed float values, if present.
        """
        attrs = {
            **super().xml_attrs,
        }

        if self.min is not None:
            attrs["min"] = str(self.min)

        if self.max is not None:
            attrs["max"] = str(self.max)

        return attrs


class Integer(ParamTypeMixin, click.types.IntParamType):
    """Integer parameter type."""

    # name = 'int'
    name = "long"  # Compatibility with the current xmlhelp interface.


class IntRange(ParamTypeMixin, click.types.IntRange):
    """Integer range parameter type.

    :param min: (optional) The minimum allowed integer value.
    :param max: (optional) The maximum allowed integer value.
    """

    name = "int_range"

    def __init__(self, min=None, max=None):
        min = int(min) if min is not None else min
        max = int(max) if max is not None else max
        super().__init__(min=min, max=max)

    @property
    def xml_attrs(self):
        """See :meth:`ParamTypeMixin.xml_attrs`.

        Includes the minimum and maximum allowed integer values, if present.
        """
        attrs = {
            **super().xml_attrs,
        }

        if self.min is not None:
            attrs["min"] = str(self.min)

        if self.max is not None:
            attrs["max"] = str(self.max)

        return attrs


class Choice(ParamTypeMixin, click.types.Choice):
    """Choice parameter type.

    :param choices: A list or tuple of valid strings to choose from.
    :param case_sensitive: (optional) Whether the choise are case sensitive. Currently
        not reflected in the generated xmlhelp.
    """

    name = "choice"

    def __init__(self, choices, case_sensitive=False):
        choices = [str(choice) for choice in choices]
        super().__init__(choices, case_sensitive=case_sensitive)

    @property
    def xml_attrs(self):
        r"""See :meth:`ParamTypeMixin.xml_attrs`.

        Includes all possible choices, separated by a single vertical bar. Bars being
        part of a choice will be escaped with a backslash.
        """
        choices = [choice.replace("|", "\\|") for choice in self.choices]

        attrs = {
            **super().xml_attrs,
            "choices": "|".join(choices),
        }

        return attrs


class Path(ParamTypeMixin, click.types.Path):
    """Path parameter type.

    Depending on the type of path to accept, the name of this parameter can change to
    ``'directory'`` or ``'file'``.

    :param exists: (optional) Flag indicating wether to check if the path actually
        exists.
    :param path_type: (optional) The type of path to accept if ``exists`` is ``True``.
        One of ``'dir'`` or ``'file'``. Defaults to ``'all'`` for both.
    """

    name = "path"

    def __init__(self, exists=False, path_type="all"):
        file_okay = dir_okay = True

        if exists:
            if path_type == "dir":
                file_okay = False
            elif path_type == "file":
                dir_okay = False

        super().__init__(exists=exists, file_okay=file_okay, dir_okay=dir_okay)

    @property
    def xml_attrs(self):
        """See :meth:`ParamTypeMixin.xml_attrs`.

        Includes the ``exists`` flag, converted to a string according to
            :meth:`Bool.to_string`.
        """
        attrs = {
            **super().xml_attrs,
            "exists": Bool.to_string(self.exists),
        }

        return attrs
