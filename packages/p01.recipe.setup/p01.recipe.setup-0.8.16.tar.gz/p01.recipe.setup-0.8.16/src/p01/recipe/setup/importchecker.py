#!/usr/bin/env python2.4
##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Import checker

This utility finds is based on the zope importchecker script, prints
out unused imports, imports that are only for tests packages and
runtime imports.

$Id: importchecker.py 5080 2021-01-21 14:44:34Z roger.ineichen $
"""
try:
    # compiler
    from p01.recipe.setup.importchecker2 import ImportDatabase
except ImportError:
    # ast
    from p01.recipe.setup.importchecker3 import ImportDatabase
import os
import os.path
import sys

from p01.recipe.setup import LoggerMixin

import zc.buildout
import zc.recipe.egg


initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
"""

env_template = """os.environ['%s'] = %r
"""


class ImportCheckerRecipe(LoggerMixin):
    """Import checker recipe."""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options

        if 'eggs' not in self.options:
            self.options['eggs'] = ''
        self.options['eggs'] = self.options['eggs'] + '\n' + 'p01.recipe.setup'
        self.egg = zc.recipe.egg.Egg(buildout, name, self.options)

    def install(self):
        dest = []
        options = self.options
        executable = self.buildout['buildout']['executable']
        path =  '"%s"' % options['path']

        # setup egg path
        # setup additional egg path
        if self.egg:
            extra_paths = self.egg.extra_paths
            eggs, ws = self.egg.working_set()
        else:
            extra_paths = ()
            ws = []

        # setup environment
        initialization = initialization_template
        env_section = self.options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in list(env.items()):
                initialization += env_template % (key, value)

        # setup checker script
        arguments = [path]
        dest.extend(zc.buildout.easy_install.scripts(
            [(self.name, 'p01.recipe.setup.importchecker', 'checker')],
            ws, executable, self.buildout['buildout']['bin-directory'],
            extra_paths = extra_paths,
            arguments = ', '.join(arguments),
            initialization = initialization,
            ))

        return dest

    update = install



def checker(path):
    """Import checker script"""

    if not os.path.exists(path):
        print("please provide a valid path %r" % path)
        sys.exit(1)

    print("*"*79)
    print("path: %r" % path)

    path = os.path.abspath(path)
    if not os.path.isdir(path):
        print("unknown path:", path)
        sys.exit(1)

    # unused imports
    db = ImportDatabase(path)
    db.findModules()
    unused_imports = db.getUnusedImports()
    module_paths = list(unused_imports.keys())
    module_paths.sort()
    print("="*79)
    print("unused imports:")
    print("="*79)
    res = []
    for path in module_paths:
        info = unused_imports[path]
        if not info:
            continue
        line2names = {}
        for name, line in info:
            names = line2names.get(line, [])
            names.append(name)
            line2names[line] = names
        lines = list(line2names.keys())
        lines.sort()
        for line in lines:
            names = ', '.join(line2names[line])
            res.append("%s:%s: %s" % (path, line, names))
    if len(res) > 0:
        for entry in res:
            print(entry)
    else:
        print("no import found")
    print()
    # testing imports
    testImports = db.getImportedModuleNames(tests=True)
    installImports = db.getImportedModuleNames(tests=False)
    print("="*79)
    print("imports for 'tests' and 'testing' packages")
    print("="*79)
    res = [name for name in testImports if name not in installImports]
    if len(res) > 0:
        for name in res:
            print(name)
    else:
        print("no import found")

    print()

    # install imports
    print("="*79)
    print("install imports")
    print("="*79)
    if len(installImports) > 0:
        for name in installImports:
            print(name)
    else:
        print("no import found")
    print("*"*79)

