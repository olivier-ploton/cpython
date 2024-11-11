"""
Some demos with 0-based and 1-based indicies, and closed slices.
"""

import builtins

########################################

class SLICER(object):
    """
    class of SLICE, used to convert an expression in brackets / braces
    into a slice(...) or extension.
    """
    def __getitem__(self, arg):
        return arg

SLICE = SLICER()

########################################

def test(*args):
    import ast
    for code in args:
        print(code, '->', end=' ')
        try:
            print(ast.unparse(ast.parse(code)))
        except Exception as e:
            print(e.__class__.__name__)

def tests():
    brackets = [
        "a[i]",
        
        "a[i:j]",
        "a[i:]",
        "a[:j]",
        "a[:]",
        
        "a[i:j:k]",
        "a[i:j:]", # a[i:j]
        "a[i::k]",
        "a[:j:k]",
        "a[i::]", # a[i:]
        "a[:j:]", # a[:j]
        "a[::k]",
        "a[::]", # a[:]

        "a[i:j::k]",
        "a[i:j::]",
        "a[:j::k]",
        "a[i:::k]", # closed a[i::k], no effect by default
        "a[i:::]",  # closed a[i:], no effect by default
        "a[:j::]",
        "a[:::]", # closed a[:], no effect by default
    ]
    test(*brackets)
    print()
    braces = [code.replace("[", "{").replace("]", "}") for code in brackets]
    test(*braces)

########################################

class _seq(object):
    def iterable(self, arg):
        """
        transforms its argument into an iterable
        """
        if isinstance(arg, slice):
            # non-integer values not taken into account
            start = 0 if arg.start is None else arg.start
            step = 1 if arg.step is None else arg.step
            if arg.stop is not None:
                return range(start, arg.stop, step)
            else:
                # unlimited iterations
                import itertools
                return itertools.count(start, step)
        else:
            # 1 iteration: arg itself
            return (arg,)
    
    def __xkey__(self, arg, braces, closed):
        if braces:
            raise IndexError("seq{...} is forbidden, use seq[...]")
        if closed:
            # For stop we can never transform an int into None,
            # because in this context, None means unlimited
            assert isinstance(arg, slice)
            start = arg.start
            stop = arg.stop
            step = 1 if arg.step is None else arg.step
            if isinstance(stop, int) and isinstance(step, int):
                stop += (step > 0) - (step < 0)
            return slice(start, stop, arg.step)
    
    def __getitem__(self, key):
        args = key if isinstance(key, tuple) else (key,)
        import itertools
        return itertools.chain(*(self.iterable(arg) for arg in args))
        
seq = _seq()

# problème pour 10:0::-1 car ça se transforme en 10:None:-1 = 10::-1
# normalement résolu avec le nouveau seq
# for i in seq[1:3::, -18, 5, 10:0::-1]: print(i)


########################################
