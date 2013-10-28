=============================
partpy
=============================

.. image:: https://badge.fury.io/py/partpy.png
   :target: http://badge.fury.io/py/partpy
    
.. image:: https://travis-ci.org/Nekroze/partpy.png?branch=master
   :target: https://travis-ci.org/Nekroze/partpy

.. image:: https://pypip.in/d/partpy/badge.png
   :target: https://crate.io/packages/partpy?version=latest


Parser Tools in Python, a collection of tools for hand writing lexers and parsers.

Parser Tools in Python (``partpy``, pronounced ``Par-Tee-Pie``), a
collection of tools for hand writing lexers and parsers in python.

There are many parser generators but there isn't much help for those
who wish to roll their own parser/lexer as counter-intuitive as that
may sound. Hand writing a parser or lexer is common practice for many highly
popular parsers and ``partpy`` provides a solid base for that through a library
of common tools.

By using ``partpy`` as the base for your own parser or lexer the hope
is to provide you with an environment where you can dive straight into
the language design, recognition and whatever else you need to do
without having to figure out how string matching should be done or
most of the error handling process.

``partpy`` supports out of the box ``Cython`` or ``RPython`` compilation
for added performance.


Features
--------

* Optional compilation with Cython or even RPython for added performance
* Object oriented basis for writing parsers
* Designed for hand written recursive decent parsers
* Powerful exception based error handling for syntax/grammar
* Both low and high level methods for parsing

