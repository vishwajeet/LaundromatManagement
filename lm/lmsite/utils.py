import os

import ConfigParser

SETTINGS_ROOT = None


def set_root(root):
    global SETTINGS_ROOT
    SETTINGS_ROOT = root

def get_abs_path(relpath):
    return (os.path.normpath(os.path.join(SETTINGS_ROOT, relpath)))

def get_setting(var, default=None):
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(SETTINGS_ROOT,'settings'))
    #print config.__dict__
    try:
        value = config.get('settings', var)
    except ConfigParser.NoOptionError, expinst:
        value = default
    return value