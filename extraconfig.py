import pkg_resources
import threading
import sys
import os

_DJANGO_IMPORTS_SETTINGS_MULTIPLE_TIMES = threading.RLock()
_already_imported = False

_EXTRA_PREFIX = '_EXTRA_'


def looks_like_settings(key):
    return key.isupper()


def should_combine(key):
    return key.startswith(_EXTRA_PREFIX)


def original_key(extra_key):
    return extra_key[len(_EXTRA_PREFIX):]


def combine(original, extra):
    try:
        return original + extra
    except TypeError:
        pass
    try:
        return original | extra
    except TypeError:
        pass
    try:
        return dict(original.items() + extra.items())
    except (AttributeError, TypeError):
        pass
    otype_name = type(original).__name__
    etype_name = type(extra).__name__
    err = "Can't combine types '%s' and '%s'." % (otype_name, etype_name)
    raise TypeError(err)


def load(entry_point_name, module_name):
    """ Scan the entry points and load extra settings. """
    entry_points = pkg_resources.iter_entry_points(entry_point_name)
    settings_module = sys.modules[module_name]
    for entry_point in entry_points:
        extra_module = entry_point.load()
        msg = "loading overrides for entrypoint '%s' located in '%s'."
        with _DJANGO_IMPORTS_SETTINGS_MULTIPLE_TIMES:
            global _already_imported
            if not _already_imported:
                print >> sys.stderr, "Process %d:" % os.getpid(),
                print >> sys.stderr, msg % (entry_point, extra_module.__file__)
            _already_imported = True
        for key, new_value in vars(extra_module).items():
            if not looks_like_settings(key):
                continue
            if should_combine(key):
                key = original_key(key)
                try:
                    original_value = getattr(settings_module, key)
                except AttributeError:
                    pass  # there's nothing to combine, act like override
                else:
                    try:
                        new_value = combine(original_value, new_value)
                    except TypeError as e:
                        raise TypeError("While combining '%s': %s" % (key, e))
            setattr(settings_module, key, new_value)
