'''
Defer: a simple library for traceable computation

Copyright 2015 Jason M. Sachs

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import operator 

numeric_ops = 'add div floordiv mod mul pow sub truediv'.split()

# this decorator from http://stackoverflow.com/questions/16698850/python-generalizing-delegating-a-method
def delegated_arithmetic(handler, rhandler):
    def add_op_method(op, cls):
        def delegated_op(self, k):
            return getattr(self, handler)(op, k)
        setattr(cls, '__{}__'.format(op), delegated_op)

    def add_reflected_op_method(op, cls):
        def delegated_op(self, k):
            return getattr(self, rhandler)(op, k)
        setattr(cls, '__r{}__'.format(op), delegated_op)

    def decorator(cls):
        for op in numeric_ops:
            add_op_method(op, cls)
            add_reflected_op_method(op, cls) # reverted operation
            add_op_method('i' + op, cls)     # in-place operation
        return cls

    return decorator

@delegated_arithmetic('_operator', '_roperator')
class DeferExpr(object):
    def _operator(self, op, k):
        return DeferBinop(op, self, k)
    def _roperator(self, op, k):
        return DeferBinop(op, k, self)
    def __getattr__(self, k):
        if not k.startswith('_'):
            return DeferAttr(self, k)
    @staticmethod
    def wrap(x):
        if isinstance(x, DeferExpr):
            return x
        else:
            return DeferConstant(x)

class DeferConstant(DeferExpr):
    def __init__(self, value, name=None):
        self._value = value
        self._name = name
    @property
    def value(self):
        return self._value
    def describe(self):
        if self._name is not None:
            return self._name
        else:
            return self._value.__repr__()        
    def __str__(self):
        if self._name is not None:
            return "%s=%s" % (self._name, self._value)
        else:
            return self._value.__str__()
    def __repr__(self):
        if self._name is not None:
            return "DeferConstant(%s,%s)" % (self._value.__repr__(), self._name.__repr__())
        else:
            return "DeferConstant(%s)" % self._value.__repr__()

class DeferBinop(DeferExpr):
    opmap = {'mul': '*',
             'div': '/',
             'mod': '%',
             'add': '+',
             'sub': '-',
             'pow': '**'}
    def __init__(self, op, a, b):
        self._op = op
        self._opf = getattr(operator, op)
        self.a = DeferExpr.wrap(a)
        self.b = DeferExpr.wrap(b)
    def __repr__(self):
        return self.describe()
    @property
    def value(self):
        return self._opf(self.a.value, self.b.value)
    def describe(self):
        return self.a.describe()+self.opmap[self._op]+self.b.describe()

class DeferAttr(DeferExpr):
    def __init__(self, obj, attr):
        self._obj = obj
        self._attr = attr
    @property
    def value(self):
        return getattr(self._obj.value, self._attr)
    def describe(self):
        return self._obj.describe()+'.'+self._attr
    def __repr__(self):
        return self.describe()
