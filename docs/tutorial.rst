Tutorial
--------

The main thing that you will use when working with partpy is the
``partpy.sourcestring.SourceString`` object. While this object can be
instantiated alone it is recommended to use it as a base class to inherit your
own lexer/parser from.

The ``SourceString`` can take a file or a string and will store it internally
along with; its length, the current index of the string, the current line and
column position and if the end of the string has been reached yet.

``SourceString`` Also has a variety of methods used for things such as;
moving the current position, matching strings or string/function patterns,
counting indentations and a few other useful things.

Movement
========

When using a ``SourceString`` it can automattically keep track of which column
and line you are on in the text file as well as which index in the string it is
currently operating on.

The most simple way to check a character and move around a ``SourceString``
derived object is with ``SourceString.get_char()`` and ``SourceString.eat_length()``,
respectively. ``.get_char()`` will simply return the character at the current
position of the ``SourceString`` and ``.eat_length()`` will move over it to the
next character.

We can use ``SourceString.has_space()``, or to avoid function call overhead,
``SourceString.eos`` to start a loop that can keep going until broken or the
entirety of the ``SourceString`` stored string has been passed.
.. testcode::

    from partpy import SourceString

    class Number(SourceString):
        digits = '0123456789'
        def spew_everything():
            while not self.eos:
                char = self.get_char()
                if char in self.digits:
                    yield char
                self.eat_length()

    parser = Number("123abc456")
    print(str(parser.spew_everything()) == '123456')

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   True

This class, when given a string to work with or a file, will go over every
character and yield only the numbers in it. While this example is trivial
and rather useless on its own it does teach us some handy things for later.

By using the ``self.eat_length()`` method, inherited from ``SourceString``,
it will automatically move the current position forward by the integer value
given to ``self.eat_length()`` which is by default 1. This will handle newline
characters and as such eating a length of 1 will move the ``SourceString``
position forwards by one along with the current column. However if the current
character is a newline then the column is set to 0 and the current line is
incremented by one.

It will always be import to eat the length of your match once you want to move
past it because all SourceString matching and retrieving methods use the
internally tracked positions.

Simple String Matching
========================

There are several ways to match strings, The most explicit way is to specifically
define each posible string to match.

``SourceString.match_string`` will attempt to match a single string at the current
position. ``SourceString.match_any_string`` does much the same thing but takes
a list of strings and will return the string that it matches and an empty string
if there is no match. There are the  accompanying method;
``SourceString.match_any_char`` are much the same as the string version but takes
a string of one or more characters to match against rather then a list.
.. testcode::

    from partpy import SourceString

    class Parser(SourceString):
        def match():
            match = self.match_any_string(['def', 'class'])
            self.eat_length(match)

            if not match:
                return match
            elif match == 'class':
                return 'TOKEN_CLASS'
            elif match == 'def':
                return 'TOKEN_DEF'

    parser = Parser('class')
    print(parser.match() == 'TOKEN_CLASS')

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   True

In an easy and fast way we can match any specific string or character however
we wish.

Pattern String Matching
=======================

``SourceString`` also has mutltiple methods to help with string and pattern
matching. For example you can match a single string or a pattern using the
following. Just to simplify the example code ``SourceString`` will directly
instanced.
.. testcode::

    from partpy import SourceString

    myMatcher = SourceString()
    myMatcher.set_string('partpy is cool')
    match = myMatcher.match_string('cool')
    if not match:
        match = myMatcher.match_function(str.isalpha)
    print(match == 'partpy')

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   True

SourceString can match text in a few ways out of the box.
``SourceString.match_string`` will attempt to match from the current position
(the very start at the moment because we haven't eaten anything yet) to the
length of the given string and will return an empty string if nothing was found.
As it will be here.

Because nothing was matched we couldn't match 'cool' at the current position we
will use ``SourceString.match_function`` instead. This method can take a function
that expects a single string or character argument and returns anything that can
be evaluated as a boolean. We will use the builtin str.isalpha method that will
return True for any alphabetical character or string.

``SourceString.match_function`` will go from the current position forwards through
the SourceString until its function does not match anymore and return the results.

There is another method, ``SourceString.match_pattern``, which works exactly the
same as ``SourceString.match_function`` but takes strings rather then functions,
this means that you can re-write the previous example as.
.. testcode::

    from partpy import SourceString

    myMatcher = SourceString()
    myMatcher.set_string('partpy is cool')
    match = myMatcher.match_string('cool')
    if not match:
        match = myMatcher.match_pattern('abcdefghijklmnopqrstuvwxyz')
    print(match == 'partpy')

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   True

This will work exactly the same and may even be faster as you can avoid function
overhead when using your own functions for ``SourceString.match_function`` however
there are many builtin str methods that are very useful and are much faster then
your own python interpreted functions.

Both ``SourceString.match_function`` and ``SourceString.match_pattern`` can actually
take two arguments. If a second argument given then the first argument is used
only to match the first character and all following characters are matched
using the second. This is useful for detecting 'Title' cased words for example.
.. testcode::

    from partpy import SourceString

    myMatcher = SourceString()
    myMatcher.set_string('Partpy is cool')
    match = myMatcher.match_function(str.isupper, str.islower)
    print(match == 'Partpy')

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   True

The two arguments may also be given as a tuple or list to the first argument
only and will be unpacked into the first and second arguments automatically.

Your Implementation
===================

As previously stated partpy was designed to be subclassed and used in your own
implementations of hand written parsers and lexical analyzers.
.. testcode::

    from partpy import SourceString

    class WordCollector(SourceString):
        def words(self):
            while not self.eos:
                while self.get_char().isspace():
                    self.eat_string(self.get_char())
                word = self.get_string()
                self.eat_string(word)
                yield word

    myCollector = WordCollector()
    myCollector.set_string('these are all words')
    words = [word for word in myCollector.words()]
    print(words == ['these', 'are', 'all', 'words'])

.. testoutput::
   :hide:
   :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

   True

This may be a pointless example in terms of its actual usefulness but ignore
that and just see how the ``SourceString`` is used rather then what this whole thing
does. One can see how they can make a simple OOP class that can parse or provide
lexical analyses using partpy in a very simple way.

Exceptions
==========

Another useful thing that one should consider using is the handy ``PartpyError``
which is an exception that can be raised with a custom message and a ``SourceString``
derived object. Using this info when the exception is raised will, by default,
add to the end of a python stacktrace a numbered list of the current line (and
the previous one if available), aswell as a carrot underneath the current character,
based on the ``SourceString`` current position. Finally it will output the custom
message if defined.

::

    >>>from partpy import SourceString, PartpyError
    >>>source = SourceString('Let's use partpy')
    >>>source.eat_length(6)
    >>>raise PartpyError(source, 'you broke it!')
    Traceback (most recent call last):
    partpy.partpyerror.PartpyError:
    1   |Let's use partpy
               ^
    you broke it!
