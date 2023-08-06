"""
Build a nested object from a serialization file
===============================================

"""

import os
import json
import yaml
import f90nml

__all__ = ["file_2_nob", "val_as_str", "path_as_str"]


def file_2_nob(path):
    """ Load a nob from a serialization file
    :params path: path to a file
    """

    ext = os.path.splitext(path)[-1]
    if ext in [".yaml", ".yml"]:
        with open(path, "r") as fin:
            nob = yaml.load(fin, Loader=yaml.SafeLoader)
    elif ext in [".json"]:
        with open(path, "r") as fin:
            nob = json.load(fin)
    elif ext in [".nml"]:
        nob = f90nml.read(path)
        # nob = nmlp.tokens
    else:
        raise RuntimeError("Format not supported")

    return nob


def val_as_str(data, max_=30):
    """return a short_string for any value"""
    if isinstance(data, dict):
        out = ""
    else:
        val_ = str(data)
        if len(val_) > max_:
            val_ = val_[:10] + " (...) " + val_[-max_ + 10 :]
        out = val_
    return out


def path_as_str(path):
    """represent path as string"""

    indent = ""
    out = ""
    for item in path:
        out += indent + "- " + item + "\n"
        indent += "  "
    return out
