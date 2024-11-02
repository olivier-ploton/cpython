# Mixing 0-based and 1-based indices with `a[i]` and `a{i}`

This is a proof-of-concept implementation of my proposal for 1-based indices and relatives. Currently implemented features:
  * 1-based indices or slices: `a{i}` means `a[i-1]`, `a{i:j:k}` means `a[i-1:j-1:k]`
  * Starred expressions are accepted, e.g. `a{i, *s, j}` means `a[i, *(h-1 for h in s), j]`
  * Closed slices with bound `j` included: `:j::`, `i:j::`, `:j::k`, `i:j::k`
  * Mixing 0-based and 1-based indices: `a[i].{j}` means `a[0-based i, 1-based j]` i.e. `a[i, j-1]`

Currently, only integer values are transformed while normalizing a 1-based or closed slice into a 0-based, semi-open slice.
Other values are left inchanged.

This implementation is a fork of the main `cpython` repository, initially `3.14.0 alpha 1`.
It is not meant to be integrated into the mainstream Python implementation.
It is the shortest path I have found to enable trying the features I propose.
Technically, it works this way:
  * No new AST node type is defined. Instead, in `Grammar/python.gram`:
      * Every index or slice inside braces, say `i`, is expanded at parse time into `FROM1[i]`.
      * Every starred expression inside braces, say `*s`, is expanded at parse time into `*STAR1[s]`.
      * Every closed slice inside brackets, say `s`, is expanded at parse time into `CLOSED0[s]`.
      * Every closed slice inside braces, say `s`, is expanded at parse time into `CLOSED0[FROM1[s]]`.
  * `FROM1`, `STAR1` and `CLOSED0` are defined in `Lib/index01.py` and exported into `builtins`
    so that they are known everywhere witout being qualified.
  * `Lib/index01` is imported in `Lib/site.py`

This implementation is meant to be fully compatible with standard Python. It passes all tests but 2, which fail for good reasons:
  * test_exceptions: `f{a + b + c}` raises SyntaxError in standard Python, but now parses as `object{index}`.
  * test_grammar: `print {1:foo}` raises SyntaxError in standard Python, but now parses as `object{slice}`.

I have commented out the failing parts of these tests (and only them).

Feel free to play with these new proposed notations. Here are some demos:
  * `XXX.py`: 

Enjoy !
