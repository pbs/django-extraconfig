import pkg_resources
import sys


EXTRA_PREFIX = '_EXTRA_'


def _get_extended_value(key, settings_module, extra_module):
    if key not in dir(settings_module):
        raise ValueError('Attempt to extend non-existing setting %s' % key)
    existing_values = getattr(settings_module, key)
    extra_values = getattr(extra_module, '%s%s' % (EXTRA_PREFIX, key))
    if type(existing_values) != type(extra_values):
        raise TypeError('Must have the same type')
    if type(existing_values) in (tuple, list):
        extended_values = existing_values + extra_values
    elif type(existing_values) is dict:
        extended_values = dict(
            existing_values.items() + extra_values.items())
    else:
        raise TypeError(
            '%s only works with tuples, lists and dicts' % EXTRA_PREFIX)
    return extended_values


def load(entry_point_name, module_name):
    """ Scan the entry points and load extra settings. """
    entry_points = pkg_resources.iter_entry_points(entry_point_name)
    settings_module = sys.modules[module_name]
    for entry_point in entry_points:
        extra_module = entry_point.load()
        for key in dir(extra_module):
            if not key.isupper():
                continue
            if key.startswith(EXTRA_PREFIX):
                key = key[len(EXTRA_PREFIX):]
                new_value = _get_extended_value(key, settings_module, extra_module)
            else:
                new_value = getattr(extra_module, key)
            setattr(settings_module, key, new_value)
