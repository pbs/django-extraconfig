import pkg_resources
import sys

def load(entry_point_name, module_name):
    """ Scan the entry points and load extra settings. """
    entry_points = pkg_resources.iter_entry_points(entry_point_name)
    settings_module = sys.modules[module_name]
    for entry_point in entry_points:
        extra_module = entry_point.load()
        for key in dir(extra_module):
            if key.isupper():
                setattr(settings_module, key, getattr(extra_module, key))
