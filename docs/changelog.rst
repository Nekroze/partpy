Changelog
---------

v0.3.0
 - Added SourceString methods:
     - eat_line
     - count_indents_last_line
     - count_indents_length_last_line
     - skip_whitespace
     - get_all_lines
     - retrieve_tokens
 - Added least argument to SourceString.match_(pattern/function) for minimum length of match
 - SourceString.eat_length now handles newlines automatically
 - Some source code cleanups and cython fixes/optimizations
 - All SourceString.eat_* methods nolonger function when SourceString.eos = 1
 - Added sphinx based documentation system and http://partpy.readthedocs.org

v0.2.1 - February 14th 2013
 - Added examples directory to sdist

v0.2.0 - February 14th 2013
 - Matcher merged into SourceString
 - new class SourceLine returned when dealing with specific SourceString lines
