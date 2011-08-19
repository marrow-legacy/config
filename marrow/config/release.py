# encoding: utf-8

"""Release information about Marrow Config."""

from collections import namedtuple


__all__ = ['version_info', 'version']


version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel', 'serial'))(0, 1, 0, 'beta', 1)

version = ".".join([str(i) for i in version_info[:3]]) + ((version_info.releaselevel[0] + str(version_info.serial)) if version_info.releaselevel != 'final' else '')




name = "marrow.config"
version = "0.1.0"
release = "0.1.0"

summary = "Useful extensions to PyYAML for use as an application configuration system in Python 2.x and 3.x."
description = """"""
author = "Alice Bevan-McGregor"
email = "alice+marrow@gothcandy.com"
url = "http://github.com/pulp/marrow.config"
download_url = "http://cheeseshop.python.org/pypi/marrow.config/"
copyright = "2010, Alice Bevan-McGregor"
license = "MIT"
