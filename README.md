# Mixing 0-based and 1-based indices with `a[i]` and `a{i}`

This is a proof-of-concept implementation of my proposal for 1-based indices and relatives.
Currently implemented features:
  * 1-based indices or slices: for `i`, `j` integers, `a{i}` means `a[i-1]`, `a{i:j:k}` means `a[i-1:j-1:k]`
  * Starred expressions are accepted, e.g. `a{i, *s, j}` means `a[i, *(h-1 for h in s), j]`
  * Closed slices with bound `j` included: `:j::`, `i:j::`, `:j::k`, `i:j::k` (with a double colon after `j`)
  * Mixing 0-based and 1-based indices in the same subscript: `a[i].{j}` means `a[0-based i, 1-based j]` i.e. `a[i, j-1]`
    
    As a comparison, `a[i]{j}` means as usual `a[0-based i][1-based j]` i.e. `a[i][j-1]`
  * Class-based customization: if the class of the indexed object `a`
    defines a method `__xkey__(self, key, braced, closed)`,
    this method is called instead of the default transformation. For example:
     * `a{i}` becomes `a[a.__xkey__(i, True, False)]`
     * `a[i:j::k]` becomes `a[a.__xkey__(i:j:k, False, True)]`
     * `a{i:j::k}` becomes `a[a.__xkey__(i:j:k, True, True)]`
    
    Otherwise, the default transformation is applied, i.e.
    integer values are transformed while normalizing a 1-based or closed slice
    into a 0-based, semi-open slice, and other values are left inchanged.

This implementation is a fork of the main `cpython` repository, initially `3.14.0 alpha 1`.
It is not meant to be integrated as-is into the mainstream Python implementation.
It is the shortest path I have found to enable trying the features I propose.
Technically, it works this way:
  * No new AST node type is defined. Instead, in `Grammar/python.gram`:
      * Every index or slice inside braces, say `i`,
        is expanded at parse time into `__xkey__(i, True, False)`.
        
      * Every starred expression inside braces, say `*s`,
        is expanded at parse time into `*__starwrapper__(__xkey__, s)`,
        which becomes at run time `*(__xkey__(i, True, False) for i in s)`.
        
      * Every closed slice inside brackets, say `i:j::k`,
        is expanded at parse time into `__xkey__(i:j:k, False, True)`.
        
      * Every closed slice inside braces, say `i:j::k`,
        is expanded at parse time into `__xkey__(i:j:k, True, True)`.

  * If some new features are used (i.e. if the `__xkey__` symbol appears),
    we have to bind `__xkey__` to the `__xkey__` of the subscripted object,
    while evaluating this subscripted object only once.
    So, `a[__xkey__(...)]` is transformed at parse time into
    `__subscriptwrapper__(a)[lambda __xkey__: __xkey__(...)]`
    which becomes (roughly) at run time `a[a.__xkey__(...)]`

  * If only standard Python subscripts are used, the grammar recognizes this fact
    and the AST is exactly the same as the AST produced by standard Python.
        
  * `__subscriptwrapper__`, `__starwrapper__` (along with the default `__xkey__`)
    are defined in `Lib/index01.py` and exported into `builtins`
    so that they are known everywhere witout being qualified.
    
  * `Lib/index01` is imported in `Lib/site.py`

This implementation is meant to be fully compatible with standard Python.
It passes all tests but 2, which fail for good reasons:
  * `test_exceptions`: `f{a + b + c}` raises SyntaxError in standard Python,
    but now parses as `object{index}`.
  * `test_grammar`: `print {1:foo}` raises SyntaxError in standard Python,
    but now parses as `object{slice}`.

I have commented out the failing parts of these tests (and only them).
I have also added unittests for the proposed features, in `test_index01.py`.

Feel free to play with these new proposed notations. Here are some demos:
  * `XXX.py`: 

Enjoy !
