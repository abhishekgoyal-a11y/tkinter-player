# Nested functions can use the arguments of parent function


# Decorators


"""
def Decorator(func):

    def wrapper(x):
        func(x)
    return wrapper


@Decorator
def printer(name):
    print(name)


# after the below code 'printer' is the 'wrapper' function
# and the 'func' function is the 'printer' function
printer = Decorator(printer)

printer('Deepak')
"""
# another decorator using functools
'''
import functools


def do_twice(func):
    @functools.wraps(func)
    def wrapper_do_twice(*args, **kwargs):
        func(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper_do_twice


@do_twice
def greet(name):
    print(f"Hello {name}")
    return 'Greet'


@do_twice
def printer():
    # print('Printer function')
    return 'Printer'


print(greet)
print(greet('Deepak'))
result = printer()
print(result)
'''
import functools
from math import factorial

"""
def debug(func):

    # Print the function signature and return value
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        # print("line1", *args,"    ", **kwargs)
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        # print("line2",args_repr,"    ", kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__} returned {value!r}")
        return value
    return wrapper_debug


@debug
def cube_of_number(dic):
    return [k**v for k, v in dic.items()]


result = cube_of_number({3: 4, 5: 2, 10: 3})

print(result)

factorial = debug(factorial)


def approximate_e(terms=18):
    return sum(1 / factorial(n) for n in range(terms))


print(approximate_e(5))
print(approximate_e(10))
"""

import random
PLUGINS = dict()


def register(func):
    """Register a function as a plug-in"""
    PLUGINS[func.__name__] = func
    return func


@register
def say_hello(name):
    return f"Hello {name}"


@register
def be_awesome(name):
    return f"Yo {name}, together we are the awesome!"


def randomly_greet(name):
    greeter, greeter_func = random.choice(list(PLUGINS.items()))
    print(f"Using {greeter!r}")
    return greeter_func(name)


print(randomly_greet('deepak'))
