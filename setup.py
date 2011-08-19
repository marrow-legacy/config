#!/usr/bin/env python
# encoding: utf-8

import os
import sys

from setuptools import setup, find_packages


if sys.version_info < (2, 6):
    raise SystemExit("Python 2.6 or later is required.")

exec(open(os.path.join("marrow", "config", "release.py")))



setup(
        name = "marrow.config",
        version = version,
        
        description = """""", # TODO: Prior to release.
        long_description = """\
For full documentation, see the README.textile file present in the package,
or view it online on the GitHub project page:

https://github.com/marrow/marrow.config""",
        
        author = "Alice Bevan-McGregor",
        author_email = "alice+marrow@gothcandy.com",
        url = "https://github.com/marrow/marrow.wsgi.objects",
        license = "MIT",
        
        install_requires = [
            'marrow.util < 2.0',
            'PyYAML'
        ],
        
        test_suite = 'nose.collector',
        tests_require = [
            'nose',
            'coverage'
        ],
        
        classifiers = [
                "Development Status :: 4 - Beta",
                "Environment :: Console",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python",
                "Topic :: Software Development :: Libraries :: Python Modules"
            ],
        
        packages = find_packages(exclude=['examples', 'tests']),
        include_package_data = True,
        package_data = {'': ['README.textile', 'LICENSE']},
        zip_safe = True,
        
        namespace_packages = ['marrow'],
    )
