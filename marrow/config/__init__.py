# encoding: utf-8

from __future__ import unicode_literals

import os
from decimal import Decimal

import yaml
from yaml.loader import Loader
from yaml.dumper import Dumper
from yaml.nodes import ScalarNode, SequenceNode
from yaml.constructor import ConstructorError
from marrow.util.compat import unicode
from marrow.util.bunch import Bunch


class Configuration(Loader):
    def construct_bunch(self, node):
        value = self.construct_mapping(node)
        data = Bunch()
        data.update(value)
        return data
    
    def construct_env(self, node):
        key = unicode(self.construct_scalar(node))
        return os.environ[key]
    
    def construct_relative(self, node):
        if not hasattr(self.stream, 'name'):
            raise ConstructorError(None, None, 'stream has no associated filename, cannot determine base directory',
                    node.start_mark)

        basedir = os.path.dirname(self.stream.name)
        path = str(self.construct_scalar(node))
        return os.path.join(basedir, path)
    
    def construct_decimal(self, node):
        value = unicode(self.construct_scalar(node))
        return Decimal(value)


class Dumper(Dumper):
    def represent_decimal(self, data):
        return self.represent_scalar('!decimal', unicode(data))


def load(src, Loader=Configuration):
    return yaml.load(src, Loader=Loader)


def dump(data, stream=None, dumper=Dumper, **kwds):
    kwds.setdefault('default_flow_style', False)
    kwds.setdefault('indent', 4)
    return yaml.dump(data, stream, dumper, **kwds)


Configuration.add_constructor('tag:yaml.org,2002:map', Configuration.construct_bunch)
Configuration.add_constructor('!env', Configuration.construct_env)
Configuration.add_constructor('!relative', Configuration.construct_relative)
Configuration.add_constructor('!decimal', Configuration.construct_decimal)
Dumper.add_representer(Decimal, Dumper.represent_decimal)
