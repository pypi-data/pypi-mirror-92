# noimport v0.0.1
A simple package to prevent the abusive use of the `import` statement in Python.
### Installation
To install, just run:
```
pip install noimport
```
### Usage
After importing the `noimport` package, any attempts of importation would result in an error
```python
>>> import noimport
>>> import time			# Built in modules won't work, ...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: import of time halted; None in sys.modules

>>> import foo			# ... nor local modules, ...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'foo'

>>> import PIL			# ... nor pip installed packages
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'PIL'
```
### License
This project is licensed under the [MIT license](https://github.com/AndyKhang404/noimport/blob/main/LICENSE)\
\
\
***Python without modules and packages, how bad can it be?***