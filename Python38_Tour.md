# Python 3.8 Has Been Released 🚀🚀 Let's Take a Tour


```python
!python --version
```

    Python 3.8.0rc1


[Launch Page](https://www.python.org/downloads/release/python-380/)

Python 3.8 is a major release of Python. Here's a roundup of some new features.

1. New Syntax Rules!
2. Parallel Data Ops Improvements!
3. Static Type Checking Features!
4. CPython Stuff!

Let's start with a new syntax rule:

## Assignment in Expressions (PEP 572)

Python now allows you to create variables inside of expressions (e.g. the body of a list comprehension.)


```python
def f(x):
    for k in range(10000000):
        x*x*x/x+x+x+x+x
    return x

x = 2

# Reuse a value that's expensive to compute
%timeit [y := f(x), y**2, y**3]

# Without reuse
%timeit [f(x), f(x)**2, f(x)**3]
```

    1.78 s ± 13.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
    5.45 s ± 93.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


Doing this in a "naked" expression is strongly discouraged in the PEP. See: [Exceptional Cases](https://www.python.org/dev/peps/pep-0572/#exceptional-cases)

[PEP 572](https://www.python.org/dev/peps/pep-0572/)

Here's one more new syntax rule:

## Positional-Only Args (PEP 570)

This one confused me until I scrolled down to the syntax section, so let's just see it in action:


```python
def prelaunch_func(foo, bar, baz=None):
    print(f"\nFoo:{foo}\nBar:{bar}\nBaz:{baz}")

def pep570_func(foo, /, bar, baz=None):
    print(f"\nFoo:{foo}\nBar:{bar}\nBaz:{baz}")
```

The `/` in the call signature of `pep570_func` denotes where the positional-only args end. These functions will let us see the practical difference PEP 570 causes.


```python
prelaunch_func(foo=1, bar=2, baz=3)
```

    
    Foo:1
    Bar:2
    Baz:3



```python
# Violating positional-only
pep570_func(foo=1, bar=2, baz=3)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-4-9e9851275486> in <module>
          1 # Violating positional-only
    ----> 2 pep570_func(foo=1, bar=2, baz=3)
    

    TypeError: pep570_func() got some positional-only arguments passed as keyword arguments: 'foo'



```python
# This is fine, as bar is right of the "/" in the call signature
pep570_func(1, bar=2, baz=3)
```

    
    Foo:1
    Bar:2
    Baz:3



```python
# This was wrong before PEP-570 of course
pep570_func(foo=1, 2, baz=3)
```


      File "<ipython-input-6-adcd14865e94>", line 2
        pep570_func(foo=1, 2, baz=3)
                           ^
    SyntaxError: positional argument follows keyword argument



What I like best about this PEP is that you can also have positional-only args with default values, as shown here:


```python
def pep570_func(foo, bar=None, baz=1, /):
    print(f"\nFoo:{foo}\nBar:{bar}\nBaz:{baz}")

pep570_func(10)
```

    
    Foo:10
    Bar:None
    Baz:1



```python
# But don't mistake them for kwargs
pep570_func(10, bar=1)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    <ipython-input-8-05c1c4b07ca6> in <module>
          1 # But don't mistake them for kwargs
    ----> 2 pep570_func(10, bar=1)
    

    TypeError: pep570_func() got some positional-only arguments passed as keyword arguments: 'bar'


For more details check out the PEP: [PEP-570](https://www.python.org/dev/peps/pep-0570/)

Now let's move on to some parallel data processing stuff:

## Shared Memory and New Pickles

Two important improvements in 3.8 were inspired by libraries like [dask](https://docs.dask.org/en/latest/) that try to solve the problem of passing data between processes. One is to create a new version of `pickle` that can pass data objects between processeses using zero-copy buffers, for more memory efficient sharing.

> The common theme of these third-party serialization efforts is to generate a stream of object metadata (which contains pickle-like information about the objects being serialized) and a separate stream of zero-copy buffer objects for the payloads of large objects. Note that, in this scheme, small objects such as ints, etc. can be dumped together with the metadata stream. Refinements can include opportunistic compression of large data depending on its type and layout, like dask does.

> This PEP aims to make pickle usable in a way where large data is handled as a separate stream of zero-copy buffers, letting the application handle those buffers optimally.

[PEP-574](https://www.python.org/dev/peps/pep-0574/#rationale)

The other biggie in this category is that processes have a new interface for sharing memory: `SharedMemory` and `SharedMemoryManager`. The docs feature a very exciting example:


```python
import multiprocessing
from multiprocessing.managers import SharedMemoryManager

# Arbitrary operations on a shared list
def do_work(shared_list, start, stop):
    for idx in range(start, stop):
        shared_list[idx] = 1

# Example from the docs
with SharedMemoryManager() as smm:
    sl = smm.ShareableList(range(2000))
    # Divide the work among two processes, storing partial results in sl
    p1 = multiprocessing.Process(target=do_work, args=(sl, 0, 1000))
    p2 = multiprocessing.Process(target=do_work, args=(sl, 1000, 2000))
    p1.start()
    p2.start()  # A multiprocessing.Pool might be more efficient
    p1.join()
    p2.join()   # Wait for all work to complete in both processes
    total_result = sum(sl)  # Consolidate the partial results now in sl
    
# `do_work` set all values to 1 in parallel
print(f"Total of values in shared list: {total_result}")
```

    Total of values in shared list: 2000


It remains to be seen if these improvements create a happy path that parallel ops focused libraries will adopt. In any case, it's exciting. Check out `SharedMemory` [here](https://docs.python.org/3.8/library/multiprocessing.shared_memory.html).

Now let's look at some staic type checking stuff:

## Typed Dictionaries (PEP 589)

Type hints don't cover nested dicts and dataclasses don't parse to JSON well enough, so now Python will support some static type-checking for dictionaries with a known set of keys. Consider the script below:

```python
# scripts/valid_589.py
from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int
        
# Cannonical assignment of Movie
movie: Movie = {'name': 'Wally 2: Rise of the Garbage Bots', 'year': 2055}
```

`mypy` will pass this with no issues because the dictionary is a valid implementation of a type.


```python
!mypy scripts/valid_589.py
```

    [1m[32mSuccess: no issues found in 1 source file[m


Now consider the invalid script below -- it has values of the wrong types:

```python
# scripts/invalid_values_589.py
from typing import TypedDict

class Movie(TypedDict):
    name: str
    year: int

def f(m: Movie):
    return m['year']

f({'year': 'wrong type', 'name': 12})
```


```python
!mypy scripts/invalid_values_589.py
```

    scripts/invalid_values_589.py:10: [1m[31merror:[m Incompatible types (expression has type [m[1m"str"[m, TypedDict item [m[1m"year"[m has type [m[1m"int"[m)[m
    scripts/invalid_values_589.py:10: [1m[31merror:[m Incompatible types (expression has type [m[1m"int"[m, TypedDict item [m[1m"name"[m has type [m[1m"str"[m)[m
    [1m[31mFound 2 errors in 1 file (checked 1 source file)[m


You can also check for missing values, invalid fields, or create `TypedDict`s that will accept missing values by using the `total=False` with the constructor.

[PEP 589](https://www.python.org/dev/peps/pep-0589)

## Finality (PEP 591)

3.8 will also implement finality. We can prevent objects from being overriden or inherited. The `@final` decorator can be used with a `class` definition to prevent inheritence, and the `Final` type will prevent overrides. Here's two examples from the PEP:

```python
# Example 1, inheriting a @final class
from typing import final

@final
class Base:
    ...

class Derived(Base):  # Error: Cannot inherit from final class "Base"
    ...

# Example 2, overriding an attribute
from typing import Final

class Window:
    BORDER_WIDTH: Final = 2.5
    ...

class ListView(Window):
    BORDER_WIDTH = 3  # Error: can't override a final attribute
```

Finality can be applied to methods, attributes and inheritence. Check out all the features in [PEP 591](https://www.python.org/dev/peps/pep-0591/)

## Literals (PEP 586)

The type hinting call signature `def f(k: int):` doesn't help us if the function expects `int`s in a range. `open` requires a `mode: str` argument from a specific set of strings. `Literal`s to the rescue!

```python
# scripts/problematic_586.py
def problematic_586(k: int):
    if k < 100:
        return k
    else:
        raise ValueError('Gotta be less than 100')
problematic_586(144)
```


```python
!mypy scripts/problematic_586.py
```

    [1m[32mSuccess: no issues found in 1 source file[m


Instead, we can pass a `Literal` to the type hinting for our argument `k`.

```python
# scripts/valid_586.py
from typing import Literal

def valid_586(k: Literal[0, 1, 2, 99]):
    if k < 100:
        return k
    else:
        return float(k)
valid_586(43)
```


```python
!mypy scripts/valid_586.py
```

    scripts/valid_586.py:8: [1m[31merror:[m Argument 1 to [m[1m"valid_586"[m has incompatible type [m[1m"Literal[43]"[m; expected [m[1m"Union[Literal[0], Literal[1], Literal[2], Literal[99]]"[m[m
    [1m[31mFound 1 error in 1 file (checked 1 source file)[m


There's a bit of nuance to using `Literal` so if you decide to explore further start with [PEP-586](https://www.python.org/dev/peps/pep-0586).

And that's it! I'm going to hold off on writing about the CPython features because, frankly, I would prefer not to write about them until I have my arms more firmly around CPython generally and those features in particular.

Thanks for reading!
