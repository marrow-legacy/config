# encoding: utf-8

from decimal import Decimal
from unittest import TestCase

from pulp.util.compat import unicode
from pulp.util.bunch import Bunch
from pulp.config import Configuration



class TestConfiguration(TestCase):
    def test_bunch(self):
        a = Configuration.load('name: value')
        self.assertEquals(a, {'name': 'value'})
        assert isinstance(a, Bunch), 'not a bunch'
    
    def test_decimal(self):
        a = Configuration.load('2.56789')
        assert isinstance(a, Decimal), 'not a decimal'
        self.assertEquals(a, Decimal('2.56789'))
        self.assertEquals(int(a), 2)
        self.assertEquals(round(a, 1), 2.6)
        
        a = Configuration.load('.inf')
        self.assertEquals(a, Decimal('Infinity'))
        
        a = Configuration.load('.nan')
        self.assertEquals(unicode(a), unicode('NaN'))
