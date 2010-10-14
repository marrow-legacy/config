# encoding: utf-8

import yaml
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.composer import Composer
from yaml.dumper import Dumper
from yaml.constructor import Constructor
from yaml.resolver import Resolver

from decimal import Decimal

from pulp.util.compat import unicode
from pulp.util.bunch import Bunch


class Configuration(Reader, Scanner, Parser, Composer, Constructor, Resolver):
    class Dumper(Dumper):
        pass
    
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        Constructor.__init__(self)
        Resolver.__init__(self)
    
    @classmethod
    def load(cls, src):
        return yaml.load(src, Loader=cls)
    
    def dump(self, destination=None):
        """Default to block-style collections."""
        
        return yaml.dump(
                self,
                destination,
                default_flow_style = False,
                indent = 4,
                Dumper = self.__class__
            )
    
    #def construct_mapping(self, node, deep=False):
    #    source = Constructor.construct_mapping(self, node, deep)
    #    return Bunch(source)
    
    def construct_yaml_bunch(self, node):
        data = Bunch()
        yield data
        value = self.construct_mapping(node)
        data.update(value)
    
    def construct_yaml_decimal(self, node):
        value = str(self.construct_scalar(node)).replace('_', '').lower()
        sign = +1
        
        if value[0] == '-': sign = -1
        if value[0] in '+-': value = value[1:]
        
        if value == '.inf':
            value = 'Infinity'
        
        elif value == '.nan':
            value = "NaN"
        
        elif ':' in value:
            digits = [Decimal(part) for part in value.split(':')]
            digits.reverse()
            base = 1
            value = 0.0
            for digit in digits:
                value += digit * base
                base *= 60
            return sign * value
        
        return sign * Decimal(value)
    
    def represent_decimal(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data)


Configuration.add_constructor(unicode('tag:yaml.org,2002:map'), Configuration.construct_yaml_bunch)
Configuration.add_constructor(unicode('tag:yaml.org,2002:python/dict'), Configuration.construct_yaml_bunch)

Configuration.add_constructor(unicode('tag:yaml.org,2002:float'), Configuration.construct_yaml_decimal)
Configuration.add_constructor(unicode('tag:yaml.org,2002:python/float'), Configuration.construct_yaml_decimal)
Configuration.add_constructor(unicode('tag:yaml.org,2002:python/Decimal'), Configuration.construct_yaml_decimal)
Configuration.Dumper.add_representer(Decimal, Configuration.represent_decimal)
