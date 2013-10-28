#!/usr/bin/env python

import os
import sys
from setuptools.command import Command

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


EXTENSIONS = []
if cy:
    EXTENSIONS.extend(partcy.EXTENSIONS)


class CleanUp(Command):
    """Cleanup all python/cython temporary or build files."""
    description = "Cleanup all python/cython temporary or build files."
    user_options = []

    def initialize_options(self):
        """pass."""
        pass

    def finalize_options(self):
        """pass."""
        pass

    def run(self):
        """Run CleanUp."""
        import fnmatch
        import shutil
        import glob
        matches = []
        matches.extend(glob.glob('./*.pyc'))
        matches.extend(glob.glob('./*.pyd'))
        matches.extend(glob.glob('./*.pyo'))
        matches.extend(glob.glob('./*.so'))
        dirs = []
        dirs.extend(glob.glob('./__pycache__'))
        dirs.extend(glob.glob('docs/_build'))
        for cleandir in [SOURCE, 'test', 'examples']:
            for root, dirnames, filenames in os.walk(cleandir):
                for filename in fnmatch.filter(filenames, '*.pyc'):
                    matches.append(os.path.join(root, filename))
                for filename in fnmatch.filter(filenames, '*.pyd'):
                    matches.append(os.path.join(root, filename))
                for filename in fnmatch.filter(filenames, '*.pyo'):
                    matches.append(os.path.join(root, filename))
                for filename in fnmatch.filter(filenames, '*.so'):
                    matches.append(os.path.join(root, filename))
                for filename in fnmatch.filter(filenames, '*.dll'):
                    matches.append(os.path.join(root, filename))
                for filename in fnmatch.filter(filenames, '*.c'):
                    matches.append(os.path.join(root, filename))
                for dirname in fnmatch.filter(dirnames, '__pycache__'):
                    dirs.append(os.path.join(root, dirname))

        for match in matches:
            os.remove(match)
        for dir in dirs:
            shutil.rmtree(dir)


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://partpy.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='partpy',
    version='1.3.0',
    description='Parser Tools in Python, a collection of tools for hand writing lexers and parsers.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Taylor "Nekroze" Lawson',
    author_email='nekroze@eturnilnetwork.com',
    url='https://github.com/Nekroze/partpy',
    packages=[
        'partpy',
    ],
    package_dir={'partpy': 'partpy'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='partpy',
    classifiers=[
        'Development Status :: 4 - beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Compilers',
        'Topic :: Text Processing :: General'
    ],
    tests_require=['pytest>=2.3.5'],
    cmdclass = {'cleanup': CleanUp},
)
