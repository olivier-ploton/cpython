"""
index01 --- an experiment to mix 0-based and 1-based indices

Defines several objects used in the modified Python grammar
in order to accept the a{i} notation and closed slices.
These objects are integrated into builtins,
so they are directly accessible (no need for qualified names).
"""

import builtins

########################################

def __default_xkey__(key, braces, closed):
    """translates a key into a standard Python one"""
    
    def from1(arg):
        """translates a 1-based slice/index into a 0-based one"""
        if isinstance(arg, int):
            return arg - 1
        elif isinstance(arg, slice):
            start = arg.start
            stop = arg.stop
            step = arg.step
            if isinstance(start, int): start -= 1
            if isinstance(stop, int): stop -= 1
            return slice(start, stop, step)
        else:
            return arg

    def closed0(arg):
        """translates a 0-based closed slice into a semi-open one"""
        assert isinstance(arg, slice)
        start = arg.start
        stop = arg.stop
        step = 1 if arg.step is None else arg.step
        if isinstance(stop, int) and isinstance(step, int):
            if step > 0:
                stop = None if stop == -1 else stop+1
            elif step < 0:
                stop = None if stop == 0 else stop-1
        return slice(start, stop, arg.step)
    
    if braces: key = from1(key)
    if closed: key = closed0(key)
    return key

class __subscriptwrapper__(object):
    """
    Expected usage: e.g. obj{i} with i integer gets transformed into:
    __subscriptwrapper__(obj)[lambda __xkey__: __xkey__(i, True, False) ]
    which itself transforms into obj[obj.__xkey__(i, True, False)]
    """
    def __init__(self, obj):
        self.obj = obj
        try:
            self.converter = obj.__xkey__
        except AttributeError:
            self.converter = __default_xkey__
        
    def __getitem__(self, key):
        return self.obj[key(self.converter)]

    def __setitem__(self, key, value):
        self.obj[key(self.converter)] = value

    def __delitem__(self, key):
        del self.obj[key(self.converter)]
    

builtins.__subscriptwrapper__ = __subscriptwrapper__

def __starwrapper__(__xkey__, args):
    """applies __xkey__ to each element of args"""
    return tuple(__xkey__(x, True, False) for x in arg)

builtins.__starwrapper__ = __starwrapper__

########################################
