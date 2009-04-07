#!/usr/bin/python -S
"""
formatters.py

This module should implement the standard list of formatters.

TODO: Specify language-independent formatters.

It also provides a method LookupChain for *composing lookup chains* for
formatters.

Formatter lookup chaining is not to be confused with plain formatter chaining,
e.g.:

  {variable|html|json}

If anyone has any better names for the two types of chaining, let the mailing
list know.
"""

__author__ = 'Andy Chu'


import os
import sys

from python import jsontemplate  # For TemplateFileInclude


def LookupChain(lookup_func_list):
  """Returns a *function* suitable for passing as the more_formatters argument
  to Template.

  NOTE: In Java, this would be implemented using the 'Composite' pattern.  A
  *list* of formatter lookup function behaves the same as a *single* formatter
  lookup funcion.

  Note the distinction between formatter *lookup* functions and formatter
  functions here.
  """
  def MoreFormatters(formatter_name):
    for lookup_func in lookup_func_list:
      formatter_func = lookup_func(formatter_name)
      if formatter_func is not None:
        return formatter_func

  return MoreFormatters


def PythonPercentFormat(format_str):
  """Use Python % format strings as template format specifiers."""

  if format_str.startswith('printf '):
    fmt = format_str[len('printf '):]
    return lambda value: fmt % value
  else:
    return None


class TemplateFileInclude(object):
  """Template include mechanism.

  The relative path is specified as an argument to the template.
  """

  def __init__(self, root_dir):
    self.root_dir = root_dir

  def __call__(self, format_str):
    """Returns a formatter function."""

    if format_str.startswith('template '):
      relative_path = format_str[len('template '):]
      full_path = os.path.join(self.root_dir, relative_path)
      f = open(full_path)
      template = jsontemplate.FromFile(f)
      f.close()
      return template.expand  # a 'bound method'

    else:
      return None  # this lookup is not applicable
