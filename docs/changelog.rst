Changelog
---------

V1.2.1
 - Fixed .pxd files not being included in source distribution

V1.2.0
 - Added Offset arguments to most SourceString methods that should support it.
 - Adde '_' to qualified identifiers

v1.1.0
 - Added SourceString.eol_distance_next
 - Added SourceString.eol_distance_last
 - Added SourceString.spew_length a reverse of eat_length
 - Minor failsafes

v1.0.0
 - Added RPython compatability.
 - Removed some dynamic features
 - Removed SourceString.generator
 - SourceString.match_pattern renamed to match_string_pattern
 - SourceString.match_function renamed to match_function_pattern
 - Pattern matching methods only take their respective types, no more lists.

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
 - Line numebers start at line 1

v0.2.1 - February 14th 2013
 - Added examples directory to sdist

v0.2.0 - February 14th 2013
 - Matcher merged into SourceString
 - new class SourceLine returned when dealing with specific SourceString lines
