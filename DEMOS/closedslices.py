"""
Using semi-open / closed slices to explicitly state
whether the upper bound is excluded or included
"""


def subscriptable(f):
    """
    @subscriptable
    def f(*args):
        ...
    
    Transforms the function f into a subscritable, non-functional object:
    we can write f[*args], and each argument can be a slice (but no kwargs).
    Because functions themselves will perhaps be subscriptable by types
    in the future (PEP 718 ?), we avoid making the resulting object callable.
    
    This should be typed, but how ?
    """
    class C(object):
        def __getitem__(self, args):
            if isinstance(args, tuple):
                return f(*args)
            else:
                return f(args)
    return C()

@subscriptable
def slices(*args):
    return args

@subscriptable
def range_(arg):
    """
    The classical range function.
    Many variations on the net (Python Discourse, StackExchange, ...)
    """
    if isinstance(arg, slice):
        start = 0 if arg.start is None else arg.start
        step = 1 if arg.step is None else arg.step
        if arg.stop is not None:
            return range(start, arg.stop, step)
        else:
            import itertools
            return itertools.count(start, step)
    else:
        raise ValueError("only range_[slice] allowed")

def iterable(arg):
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
            import itertools
            return itertools.count(start, step)
    else:
        return (arg,)


@subscriptable
def seq(*args):
    print(args)
    import itertools
    return itertools.chain(*(iterable(arg) for arg in args))

# problème pour 10:0::-1 car ça se transforme en 10:None:-1 = 10::-1
for i in seq[1:3::, -18, 5, 10:1::-1]: print(i)
