

# testing how to produce lists of folders to pass to setup.py

from __future__ import print_function
import os


def get_files(folder):
    """walk dir and return .* files as a list
    Note: directories are walked recursively"""
    out = []
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            out.append(os.path.join(root, dir))
    return out



def get_package_folders(top_folder, root_path):
    """generate dynamically the list of folders needed by the package_data setting
    ..
        package_data={
             'ontospy': ['viz/static/*.*', 'viz/templates/*.*', 'viz/templates/shared/*.*', 'viz/templates/splitter/*.*', 'viz/templates/markdown/*.*'],
        },
    ...
    """
    _dirs = []
    out = []
    for root, dirs, files in os.walk(top_folder):
        for dir in dirs:
            _dirs.append(os.path.join(root, dir))
    for d in _dirs:
        _d = os.path.join(d, "*.*")
        out.append(_d.replace(root_path+"/", ""))
    return out


here = os.path.abspath(os.path.dirname(__file__))
one_level_up = os.path.dirname(here)

static_folder = os.path.join(one_level_up, "viz", "static")
templates_folder = os.path.join(one_level_up, "viz", "templates")

print(static_folder)
#
# for f in get_files(static_folder):
#     print os.path.join(f, "*.*")
#     # print f.replace(one_level_up, "")

res = get_package_folders(static_folder, one_level_up) + get_package_folders(templates_folder, one_level_up)
for r in res:
    print(r)
