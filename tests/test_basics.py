# encoding: utf-8

from __future__ import unicode_literals

import os
from io import BytesIO
from decimal import Decimal
from unittest import TestCase

from yaml.constructor import ConstructorError
from marrow.util.compat import unicode
from marrow.util.bunch import Bunch

from marrow.config import load, dump



class TestConfiguration(TestCase):
    def test_bunch(self):
        a = load('name: value')
        self.assertEquals(a, {'name': 'value'})
        assert isinstance(a, Bunch), 'not a bunch'
    
    def test_decimal(self):
        a = load('!decimal 2.56789')
        assert isinstance(a, Decimal), 'not a decimal'
        self.assertEquals(a, Decimal('2.56789'))
        self.assertEquals(int(a), 2)
        self.assertEquals(round(a, 1), 2.6)
        
        a = load('!decimal Infinity')
        self.assertEquals(a, Decimal('Infinity'))
        
        a = load('!decimal NaN')
        self.assertEquals(unicode(a), unicode('NaN'))

    def test_env(self):
        os.environ['TEST_ENTRY'] = 'foo'
        a = load('!env TEST_ENTRY')
        del os.environ['TEST_ENTRY']
        self.assertEquals(a, 'foo')

    def test_relative(self):
        stream = BytesIO(b'!relative some/path')
        stream.name = '/tmp/foo/test.yaml'
        a = load(stream)
        self.assertEquals(a, '/tmp/foo%ssome/path' % os.path.sep)

    def test_relative_nofilename(self):
        stream = BytesIO(b'!relative some/path')
        self.assertRaises(ConstructorError, load, stream)


class TestDumper(TestCase):
    def test_represent_decimal(self):
        self.assertEquals(dump(Decimal('-1.2321')), '!decimal -1.2321\n')
