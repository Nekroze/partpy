Tutorial
--------

Starting a new parser or lexer with partpy is made very easy as all
functionality is provided by subclassing either partpy.SourceString.

SourceString
============

A SourceString can store a string (or load if from a file) and then use multiple
methods to get characters from that string and move the current cursor position
forward through it. For example::
    from partpy import SourceString

    mySource = SourceString()
    mySource.set_string('hello world')
    mySource.eat_string('hello ')
    assert mySource.get_char() == 'w'

This simple example creates a new SourceString and gives it a string to store.
Then it moves the current position counter forward by eating 'hello ',
This could also be accomplished by using ``SourceString.eat_length(6)`` however
eat_string will detect newlines and move the column and row position counters
forwards automatically. The last line gets the character at the current position
that the SourceString has counted to and makes sure it is a 'w' as would be expected.

Matcher
=======

SourceString also has mutltiple methods to help with string and pattern matching.
For example you can match a single string or a pattern using the following::
    from partpy import SourceString

    myMatcher = SourceString()
    myMatcher.set_string('partpy is cool')
    match = myMatcher.match_string('cool')
    if not match:
        match = myMatcher.match_function(str.isalpha)
    assert match == 'partpy'

SourceString can match text in a few ways out of the box.
SourceString.match_string will attempt to match from the current position
(the very start at the moment because we haven't eaten anything yet) to the
length of the given string and will return an empty string if nothing was found.

Because nothing we couldn't match 'cool' at the current position we will use
``SourceString.match_function`` instead. This method can take a function that
expects a single string or character argument and returns anything that can
be evaluated as a boolean. We will use the builtin str.isalpha method that will
return True for any alphabetical character or string.

``SourceString.match_function`` will go from the current position forwards through
the SourceString until its function does not match anymore and
return the results.

There is another method, ``SourceString.match_pattern``, which works exactly the
same as ``SourceString.match_function`` but takes strings rather then functions,
this means that you can re-write the previous example as::
    from partpy import SourceString

    myMatcher = SourceString()
    myMatcher.set_string('partpy is cool')
    match = myMatcher.match_string('cool')
    if not match:
        match = myMatcher.match_pattern('abcdefghijklmnopqrstuvwxyz')
    assert match == 'partpy'

This will work exactly the same and may even be faster as you can avoid function
overhead when using your own functions for ``SourceString.match_function`` however
there are many builtin str methods that are very useful and are much faster then
your own python interpreted functions.

Both ``SourceString.match_function`` and ``SourceString.match_pattern`` can actually
take two arguments. If a second argument given then the first argument is used
only to match the first character and all following characters are matched
using the second. This is useful for detecting 'Title' cased words for example::
    from partpy import SourceString

    myMatcher = SourceString()
    myMatcher.set_string('Partpy is cool')
    match = myMatcher.match_function(str.isupper, str.islower)
    assert match == 'Partpy'

The two arguments may also be given as a tuple or list to the first argument
only and will be unpacked into the first and second arguments automatically.

Your Implementation
===================

Previous examples have used the SourceString class directly. However partpy is
meant to provide a base class that you can inherit your own classes from so that
all provided functionality can be accessed as methods of self. This makes
everything much easier and cleaner while keeping with the popular OOP design
in use today.::
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
    assert words == ['these', 'are', 'all', 'words']

This may be a pointless example in terms of its actual usefulness but ignore
that and just see how the SourceString is used rather then what this whole thing
does. One can see how they can make a simple OOP class that can parse or provide
lexical analyses using partpy in a very simple way.
