# open-close-mixin

## About
Easy pluggable Mixin (and decorators) for objects that may benefit from open-close dynamics.

## Installing 
You can simply install it using *pip* as follows:
```console
$ pip install open-close-mixin
```

## Usage
You may import an `OpenCloseMixin` along some other decorators from the package root and use them further on to create your own class with open and close dynamics!
```python
>>> from open_close_mixin import OpenCloseMixin, always

>>> class Foo(OpenCloseMixin):
>>>     # only while open, that's default behaviour
>>>     def run_when_open(self):
>>>         print("The instance is open so I was able to run")
>>> 
>>>     @always
>>>     def run_always(self):
>>>         print("I am ALWAYS able to run, whether the instance is open or not")
>>> 
>>> f = Foo()
>>> f.open()
>>> f.run_always()
I am ALWAYS able to run, whether the instance is open or not
>>> 
>>> f.run_when_open()
The instance is open so I was able to run
>>> 
>>> f.close()
>>> f.run_always()
I am ALWAYS able to run, whether the instance is open or not
>>> 
>>> f.run_when_open()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/alberto/Projects/personal/open-close-mixin/open_close_mixin/decorators.py", line 27, in wrapper
    raise exception from None
ValueError: The instance is not open and the method "Foo.run_when_open" cannot run under such condition.
```
