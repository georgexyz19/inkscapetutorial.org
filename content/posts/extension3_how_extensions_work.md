title: How Extensions Work
slug: how-extensions-work
date: 2021-07-28 08:42
category: extension
chapter: 3
note: How Extensions Work

## Class Initialization

The last two lines of `triangle.py` files are shown below. The first line is 
boilerplate code. If we run this module on terminal, the Python interpreter will set the 
`__name__` to `__main__` and the code `Triangle().run()` will execute. 

```python
if __name__ == '__main__':
    Triangle().run()
```

The first part of the second line `Triangle()` initializes an instance of 
`Triangle` class. We can think of the `Triangle().run()` as two statements like this. 

```python
t = Triangle()
t.run()
```

In this section we will discuss class initialization part `t = Triangle()`, and 
in the next section we will examine the run part `t.run()`. 

The class `Triangle` itself does not define an `__init__` method, and 
the `__init__` methods in superclasses will be invoked automatically. The 
diagram below shows the superclasses of `Triangle`.  

<div style="max-width:600px">
  <img class="img-fluid pb-2" src="/images/ext3/extension-classes.svg" alt="classes"> 
</div>

Both `SvgInputMixin` and `InkscapeExtension` classes have `__init__` methods, and
those will be invoked. 

Here is the code in the `__init__` method of `SvgInputMixin` class.  It simply calls
`add_argument` method twice.  The `super().__init__()` statement invokes `__init__` 
method in `object` because `super` refers to `object`. 

```python
# __init__ in SvgInputMixin class, base.py
def __init__(self):
    super().__init__()

    self.arg_parser.add_argument(
        "--id", action="append", type=str, dest="ids", default=[],
        help="id attribute of object to manipulate")

    self.arg_parser.add_argument(
        "--selected-nodes", action="append", type=str, 
        dest="selected_nodes", default=[],
        help="id:subpath:position of selected nodes, if any")
```


Let's look at the `__init__` method in `InkscapeExtension` class next. 

```python
# __init__ in InkscapeExtension class 
def __init__(self):
    # type: () -> None
    NSS.update(self.extra_nss)
    self.file_io = None # type: Optional[IO]
    self.options = Namespace()
    self.document = None # type: Union[None, bytes, str, etree]
    self.arg_parser = ArgumentParser(description=self.__doc__)

    self.arg_parser.add_argument(
        "input_file", nargs="?", metavar="INPUT_FILE", 
        type=filename_arg, default=None,
        help="Filename of the input file (default is stdin)")

    self.arg_parser.add_argument(
        "--output", type=str, default=None,
        help="Optional output filename for saving " +
            "the result (default is stdout).")

    self.add_arguments(self.arg_parser)

    localize()
```

The `NSS.update(...)` line is for XML namespaces.  The `NSS` itself is an abbreviation
for *Namespace Specific String*. 

The `__init__` method initializes four instance variables `file_io`, `options`, 
`document`, and `arg_parser`. It calls the `add_argument` methods of `ArgumentParser` 
class twice, and then it calls the `add_arguments` class method.  The `add_arguments` method 
is overridden in `Triangle` class, so the `add_arguments` method in the `Triangle` class 
will be called. The method calls `add_argument` of `ArgumentParser` class seven times. 
Note the method name is `add_argument` in `ArgumentParser` class and it is `add_arguments` 
(notice the plural) in `Triangle` class. 

```python
# add_argument method in Triangle class
def add_arguments(self, pars):
    logging.debug(f'Triangle add_arguments method starts')  ##
    pars.add_argument("--s_a", type=float, 
        default=100.0, help="Side Length a")
    pars.add_argument("--s_b", type=float, 
        default=100.0, help="Side Length b")
    pars.add_argument("--s_c", type=float, 
        default=100.0, help="Side Length c")
    pars.add_argument("--a_a", type=float, 
        default=60.0, help="Angle a")
    pars.add_argument("--a_b", type=float, 
        default=30.0, help="Angle b")
    pars.add_argument("--a_c", type=float, 
        default=90.0, help="Angle c")
    pars.add_argument("--mode", default='3_sides', 
        help="Side Length c")
    logging.debug(f'Triangle add_arguments method ends')  ##
```

We can add a pair of logging statements at the beginning and end of the method call to 
find out the call sequence.  The similar statements are added to the two `__init__` 
methods, and the result is shown below. 

```
DEBUG: SvgInputMixin __init__ starts 
DEBUG: InkscapeExtension __init__ starts
DEBUG: Triangle add_arguments method starts
DEBUG: Triangle add_arguments method ends
DEBUG: InkscapeExtension __init__ ends
DEBUG: SvgInputMixin __init__ ends
```

The interesting part here is that the `__init__` method in `SvgInputMixin` is called 
first.  When the Python interpreter encounters the `self.arg_parser` instance variable, 
it can't find the definition.  It suspends this `__init__` method call and starts 
invoking `__init__` method in `InkscapeExtension` class. The `add_arguments` method 
starts and ends as expected because it is called within the `__init__` method of 
`InkscapeExtension`.  The `__init__` method in `InkscapeExtension` class returns first, 
and then the `__init__` method in `SvgInputMixin` class returns.  This is something in 
Python I don't know until I work on this example.  There are always new things to 
learn in Python.  

## Run Method

After the initialization, the `run` method is where everything happens. Here is 
the code of `run` method in `InkscapeExtension` class. 

```python
def run(self, args=None, output=stdout):
    # type: (Optional[List[str]], Union[str, IO]) -> None
    """Main entrypoint for any Inkscape Extension"""
    try:
        if args is None:
            args = sys.argv[1:]

        self.parse_arguments(args)

        if self.options.input_file is None:
            self.options.input_file = sys.stdin

        if self.options.output is None:
            self.options.output = output

        self.load_raw()
        self.save_raw(self.effect())
    except AbortExtension as err:
        err.write()
        sys.exit(ABORT_STATUS)
    finally:
        self.clean_up()

```

Let's take a close look at the code between `try` and `except` lines. 
From last chapter, we know that the `sys.argv` value is a list of arguments. 
The `args` value is a list starting from the second item. 

```
['triangle.py', '--s_a=100', '--s_b=100', 
   '--s_c=100', '--a_a=60', '--a_b=30', '--a_c=90', 
   '--mode=3_sides', '/tmp/ink_ext_XXXXXX.svgVYXM70']
```

The `parse_arguments` method in `InkscapeExtension` class simply calls 
`parse_args` method of `arg_parser` object. The returned value is assigned 
to the `options` instance variable, which is a `Namespace` object. 


```python
def parse_arguments(self, args):
    # type: (List[str]) -> None
    """Parse the given arguments and set 'self.options'"""
    self.options = self.arg_parser.parse_args(args)
```

After the `parse_arguments` method call, the `self.options` value is 
the `Namespace` object shown below. We can access variables in the object like 
a property (e.g., `self.options.input_file`). Notice the `ids` and `selected_nodes` 
instance variables in `Namespace`.  Those are the values Inkscape passes to the 
extension.   

```
Namespace(input_file='/tmp/ink_ext_XXXXXX.svgVJUG70', 
          output=None, s_a=100.0, s_b=100.0, s_c=100.0, 
          a_a=60.0, a_b=30.0, a_c=90.0, mode='3_sides', 
          ids=[], selected_nodes=[]) 
```

The next four statements changes the `self.options.output` and `self.options.input_file` 
values if they are `None`. The `self.options.input_file` does not change in 
the `Triangle` example.  The value `/tmp/ink_ext_XXXXXX.svgVJUG70` is a 
temporary file Inkscape creates and passes to the extension. 

We can think of the last two lines as the three lines shown below. 
Upon this point, the program is working on initialization and setting up 
variables. These three lines of code is doing the actually work, loading 
the temporary svg file, modifying it, and sending it back to Inkscape. 
We will examine those method calls in the next chapter. 

```python
self.load_raw()
e = self.effect()
self.save_raw(e)
```

## Python ArgParse Module

From the above discussion, we should have a basic understanding on how Inkscape extensions 
work. When we launch Inkcape, it will check files under user extension 
and system extension directories, and create menu items under the `Extensions` 
top level menu.  

When we click an extension menu such as `Triangle`, Inkscape will setup the 
input and output stream of Python environment and call the Python interpreter 
installed at this path `/usr/bin/python3`.  It also passes the following 
arguments to the Python interpreter. 

```
['triangle.py', '--s_a=100', '--s_b=100', 
   '--s_c=100', '--a_a=60', '--a_b=30', '--a_c=90', 
   '--mode=3_sides', '/tmp/ink_ext_XXXXXX.svgVYXM70']
```

This is similar to enter a command on a bash terminal. 

```
$/usr/bin/python3 triangle.py --s_a=100 --s_b=100 --s_c=100 \
    --a_a=60 --a_b=30 --a_c=90 --mode=3_sides \
    /tmp/ink_ext_XXXXXX.svgVYXM70
```

The `argparse` is the Python standard library module which turns command 
line options (like `--s_a=100`) and arguments (like `/tmp/ink...`) into 
variables we can access (`self.options.s_a`) in the program. 

Python documentation site has an 
[official argparse module tutorial](https://docs.python.org/3/howto/argparse.html). 
The `argparse` module was introduced in Python 3.4, which supersedes the `optparse` 
in Python2. The old Inkscape extensions before Inkscape 1.0 use `optparse` module. 

