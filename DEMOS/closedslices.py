"""
Using semi-open / closed slices to explicitly state
whether the upper bound is excluded or included
"""

def PRINT(*args, **kwargs):
    hrule = '-' * 60
    print()
    print(hrule)
    print(*args, **kwargs)
    print(hrule)
    print()

########################################

PRINT("Using range_[i:j::k] to explicitly include upper bound")

class _range_:
    """
    A use case for closed slices: transform a slice into a finite iterable
    Well-known idea (folklore), countless messages about it on the net.
    range[i:j:k] essentially abbreviates range(i, j, k).
    range[i:j::k] is very useful to express that j must be included
    """
    def __getitem__(self, key):
        if isinstance(key, slice):
            step = 1 if key.step is None else key.step
            start = 0 if key.start is None else key.start                
            stop = (step > 0) - (step < 0) if key.stop is None else key.stop
            return range(start, stop, step)
        elif isinstance(key, tuple):
            raise ValueError("range_[i1, i2, ...] is forbidden")
        else:
            raise ValueError("range_[n] is forbidden, use range(n) instead")
        
        import itertools
        return itertools.chain(*(self.iterable(arg) for arg in args))

range_ = _range_()

n = 10
print(f"{sum(1/i**2 for i in range(1, n+1)) = }")
print(f"{sum(1/i**2 for i in range_[1:n::]) = }")
print()

print(f"{[i for i in range_[:n]] = }")
print(f"{[i for i in range_[:n::]] =}")
print(f"{[i for i in range_[1:n::]] = }")
print()

print(f"{[i for i in range_{n::-1}]        = }")
print(f"{[i for i in reversed(range_[:n])] = }")
print()

print(f"{[i for i in range_{n:1:-1}]        = }")
print(f"{[i for i in reversed(range_[1:n])] = }")
print()

print(f"{[i for i in range_[-n:]] = }")
print(f"{[i for i in range_[-n:0]] = }")

########################################

PRINT("seq: multiple ranges chained (closed slices, custom __xkey__)")

class _seq:
    """
    A use case for closed slices, and for custom __xkey__:
    transform a list of slices into a potentially infinite iterable.
    
    Without a custom __xkey__, seq[n:0::-1] is transformed in a context of
    finite lists where :0:: means "beginning included" and becomes seq[n::-1].
    But this means seq[n:-oo:-1] in the context of inifinite iterations.
    A custom __xkey__ solves this issue.
    """
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
            raise ValueError("seq{...} is forbidden, use seq[...]")
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

n = 10
print(f"{sum(1/i**2 for i in range(1, n+1)) = }")
print(f"{sum(1/i**2 for i in    seq[1:n::]) = }")
print()

# With seq[...] we have to manage a potentially infinite iterable
def limited(iterable, maxlength=20):
    """
    convert a potentially infinite iterable into a list with
    at most maxlength elements (and an extra Ellipsis)
    """
    result = []
    l = 0
    for i in iterable:
        result.append(i)
        l += 1
        if l >= maxlength:
            result.append(...)
            break
    return result

print(f"{limited(seq[1:3::]) = }")
print(f"{limited(seq[1:3::, 100, 3:1::-1]) = }")
print(f"{limited(seq[5::10]) = }")

########################################

PRINT("Math: inverse of a permutation of {1, 2, ..., n}")

# A permtation: each value between 1 and n inclusive appears exactly once
p = [1, 5, 3, 2, 4]
print(f"{p = }")

# Let us compute q = p⁻¹
q = [None] * len(p)
for i in seq[1:len(p)::]: q{p{i}} = i
print(f"{q = }")

# Same computation wit 0-based indices
q = [None] * len(p)
for i in range(len(p)): q[p[i]-1] = i+1
print(f"{q = }")

########################################
