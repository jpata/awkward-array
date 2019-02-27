import itertools
import sys
import numpy

from collections import OrderedDict
from numpy.core import umath as um

try:
    from pandas.core.arrays import ExtensionArray
except ImportError:
    raise ImportError('Awkward-pandas requires pandas >= 0.23')

if sys.version_info[0] <= 2:
    izip = itertools.izip
    string = basestring
    unicode = unicode
else:
    izip = zip
    string = str
    unicode = str

# FIXME: this goes away once everything starts depending on 0.8.0
frombuffer = numpy.frombuffer

# FIXME: this goes away once everything starts depending on 0.8.0
def toarray(value, defaultdtype, passthrough=None):
    import awkward.array.base
    return awkward.array.base.AwkwardArray._util_toarray(value, defaultdtype, passthrough=passthrough)

def awkwardlib(awkwardlib):
    if awkwardlib is None:
        import awkward
        return awkward
    elif isinstance(awkwardlib, str):
        return importlib.import_module(awkwardlib)
    else:
        return awkwardlib

class bothmethod(object):
    def __init__(self, fcn):
        self.fcn = fcn
    def __get__(self, ins, typ):
        if ins is None:
            return lambda *args, **kwargs: self.fcn(True, typ, *args, **kwargs)
        else:
            return lambda *args, **kwargs: self.fcn(False, ins, *args, **kwargs)
def _disables_array_ufunc(obj):
    """True when __array_ufunc__ is set to None."""
    try:
        return obj.__array_ufunc__ is None
    except AttributeError:
        return False

def _binary_method(ufunc, name):
    """Implement a forward binary method with a ufunc, e.g., __add__."""
    def func(self, other):
        if _disables_array_ufunc(other):
            return NotImplemented
        return ufunc(self, other)
    func.__name__ = '__{}__'.format(name)
    return func

def _reflected_binary_method(ufunc, name):
    """Implement a reflected binary method with a ufunc, e.g., __radd__."""
    def func(self, other):
        if _disables_array_ufunc(other):
            return NotImplemented
        return ufunc(other, self)
    func.__name__ = '__r{}__'.format(name)
    return func

def _inplace_binary_method(ufunc, name):
    """Implement an in-place binary method with a ufunc, e.g., __iadd__."""
    def func(self, other):
        return ufunc(self, other, out=(self,))
    func.__name__ = '__i{}__'.format(name)
    return func

def _numeric_methods(ufunc, name):
    """Implement forward, reflected and inplace binary methods with a ufunc."""
    return (_binary_method(ufunc, name),
            _reflected_binary_method(ufunc, name),
            _inplace_binary_method(ufunc, name))

def _unary_method(ufunc, name):
    """Implement a unary special method with a ufunc."""
    def func(self):
        return ufunc(self)
    func.__name__ = '__{}__'.format(name)
    return func

class NDArrayOperatorsMixin(ExtensionArray):
    __lt__ = _binary_method(um.less, 'lt')
    __le__ = _binary_method(um.less_equal, 'le')
    __eq__ = _binary_method(um.equal, 'eq')
    __ne__ = _binary_method(um.not_equal, 'ne')
    __gt__ = _binary_method(um.greater, 'gt')
    __ge__ = _binary_method(um.greater_equal, 'ge')

    # numeric methods
    __add__, __radd__, __iadd__ = _numeric_methods(um.add, 'add')
    __sub__, __rsub__, __isub__ = _numeric_methods(um.subtract, 'sub')
    __mul__, __rmul__, __imul__ = _numeric_methods(um.multiply, 'mul')
    if sys.version_info.major < 3:
        # Python 3 uses only __truediv__ and __floordiv__
        __div__, __rdiv__, __idiv__ = _numeric_methods(um.divide, 'div')
    __truediv__, __rtruediv__, __itruediv__ = _numeric_methods(
        um.true_divide, 'truediv')
    __floordiv__, __rfloordiv__, __ifloordiv__ = _numeric_methods(
        um.floor_divide, 'floordiv')
    __mod__, __rmod__, __imod__ = _numeric_methods(um.remainder, 'mod')
    if hasattr(um, "divmod"):
        __divmod__ = _binary_method(um.divmod, 'divmod')
        __rdivmod__ = _reflected_binary_method(um.divmod, 'divmod')
    # __idivmod__ does not exist
    # TODO: handle the optional third argument for __pow__?
    __pow__, __rpow__, __ipow__ = _numeric_methods(um.power, 'pow')
    __lshift__, __rlshift__, __ilshift__ = _numeric_methods(
        um.left_shift, 'lshift')
    __rshift__, __rrshift__, __irshift__ = _numeric_methods(
        um.right_shift, 'rshift')
    __and__, __rand__, __iand__ = _numeric_methods(um.bitwise_and, 'and')
    __xor__, __rxor__, __ixor__ = _numeric_methods(um.bitwise_xor, 'xor')
    __or__, __ror__, __ior__ = _numeric_methods(um.bitwise_or, 'or')

    # unary methods
    __neg__ = _unary_method(um.negative, 'neg')
    if hasattr(um, "positive"):
        __pos__ = _unary_method(um.positive, 'pos')
    __abs__ = _unary_method(um.absolute, 'abs')
    __invert__ = _unary_method(um.invert, 'invert')