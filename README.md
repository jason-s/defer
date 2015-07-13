# Defer: a simple library for traceable computation #

One of the benefits of computers is that they can easily evaluate
mathematical expressions with great accuracy and speed. On the other
hand, it can be very clumsy making a report of those expressions.

For example, suppose you need to calculate `x=3*99`:

    >>> x = 3*99
    >>> print x
    297
    
You get the answer, but where is the context? It is missing. We have to do this:

    >>> x = 3*99
    >>> print "x = 3*99 = ", x
    x = 3*99 =  297

But that's not good, because now we have to repeat the expression twice, once
in the evaluation, and once in the report, and these can get out of sync.

The Defer library is a way of producing computations that can both be evaluated
*and* described, so that the results can be kept in sync. For example:

    >>> k = DeferConstant(5.21,'k')
    >>> m = 2+k*7%3
    >>> m.value
    2.469999999999999
    >>> m
    2+k*7%3
    
Defer is published under the [Apache License](http://www.apache.org/licenses/LICENSE-2.0.html)
and can be easily incorporated into Python applications.
    
