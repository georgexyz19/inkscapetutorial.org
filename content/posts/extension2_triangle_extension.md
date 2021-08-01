title: Triangle Extension Code
slug: triangle-extension-code
date: 2021-07-27 08:42
category: extension
chapter: 2
note: Triangle extension code explained

## Extension Structure

In this tutorial, we will take a detailed look at the `Triangle` extension code.
Usually an Inkscape extension consists of two files, one `.inx` file and 
one `.py` file. The `.inx` file contains xml code and the `.py` file is the 
Python file. The `.py` file ususally imports other modules so an extension 
involves multiple Python files. 

The `Triangle` extension code is in the `triangle.inx` and `triangle.py` 
files. Let's open those two files in a text editor. 

## Inx File

The `triangle.inx` file only has 27 lines. The content of the file is shown below.

```xml
<?xml version="1.0" encoding="UTF-8"?> ➊
<inkscape-extension
    xmlns="http://www.inkscape.org/namespace/inkscape/extension">
    <name>Triangle</name>    ➋
    <id>math.triangle</id>   ➌
    <param name="s_a" type="float" min="0.01" max="10000"  
        gui-text="Side Length a (px):">100.0</param>  ➍
    <param name="s_c" type="float" min="0.01" max="10000" 
        gui-text="Side Length c (px):">100.0</param>
    <param name="a_a" type="float" min="0"    max="180"   
        gui-text="Angle a (deg):">60</param>
    <param name="a_b" type="float" min="0"    max="180"   
        gui-text="Angle b (deg):">30</param>
    <param name="a_c" type="float" min="0"    max="180"   
        gui-text="Angle c (deg):">90</param>
    <param name="s_b" type="float" min="0.01" max="10000" 
        gui-text="Side Length b (px):">100.0</param>
    <param name="mode" type="optiongroup" appearance="combo"     
        gui-text="Mode:">  ➎
        <option value="3_sides">From Three Sides</option>
        <option value="s_ab_a_c">From Sides a, b and Angle c</option>
        <option value="s_ab_a_a">From Sides a, b and Angle a</option>
        <option value="s_a_a_ab">From Side a and Angles a, b</option>
        <option value="s_c_a_ab">From Side c and Angles a, b</option>
    </param>
    <effect>
        <object-type>all</object-type>
        <effects-menu>
            <submenu name="Render"/> ➏
        </effects-menu>
    </effect>
    <script>
        <command location="inx" 
            interpreter="python">triangle.py</command> ➐
    </script>
</inkscape-extension>
```
Here is a list of short descriptions for lines with circled numbers. 

1. this line indicates it is an xml file
2. name tag, specifies the name on submenu (Render -> Triangle)
3. id tag, unique id of the extension
4. param tag, specifies an input control on the diagbox
5. param tag, specifies a select control 
6. submenu tag, shows up as a submenu (Extensions -> Render)
7. command tag, the name of the Python file to run


The first line and `inkscape-extension` tag are boilerplate code. Every 
extension has those lines.  Inside the `inkscape-extension` tag, there 
are `name`, `id`, `param`, `effect`, and `script` tages. 

The `name` tag value `Triangle` shows up as the menu name. The second 
level menu `Render` under `Extensions` menu is specified in the `submenu` tag 
under `effect`.  

The `id` value must be unique for each extension. We can add 
a namespace such as `math.` before the `triangle` to make it distinctive. 

The `param` tags represent input controls on the dialog. This `Triangle` extension 
includes two types of param element float and optiongroup. There are many other 
types we can use.  This 
[Inkscape wiki page](https://wiki.inkscape.org/wiki/Extensions:_INX_widgets_and_parameters) 
has a complete list and relevent information. 

The `command` tag under the `script` element indicates that the extension 
code is a Python program in `triangle.py` file. When we click the `apply` 
button on the dialog, the `triangle.py` Python program will start running. 

The `.inx` file is in XML format. 
XML stands for *extensible markup language*, which is a popular file format 
in the early 2000s. I still remember attending a seminar in colleage and the 
speaker says something like every one should learn XML and write in XML. The 
format becomes less popular over time, but the default Inkscape file format 
SVG is also in XML format. 

## Python File

The `triangle.py` file has 188 lines. Part of the content is shown below.  

```python
import sys
from math import acos, asin, cos, pi, sin, sqrt

import inkex

X, Y = range(2)

def draw_SVG_tri(point1, point2, point3, offset, 
    width, name, parent):
    ...
......

def draw_tri_from_3_sides(s_a, s_b, s_c, offset, width, parent):  
    if is_valid_tri_from_sides(s_a, s_b, s_c):
        a_b = angle_from_3_sides(s_a, s_c, s_b)

        a = (0, 0)  
        b = v_add(a, (s_c, 0))  
        c = v_add(b, pt_on_circ(s_a, pi - a_b))  
        c[1] = -c[1]

        offx = max(b[0], c[0]) / 2 
        offy = c[1] / 2 
        offset = (offset[0] - offx, offset[1] - offy)  

        draw_SVG_tri(a, b, c, offset, width, 'Triangle', parent)
    else:
        inkex.errormsg('Invalid Triangle Specifications.')


class Triangle(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--s_a", type=float, default=100.0, 
            help="Side Length a")
        pars.add_argument("--s_b", type=float, default=100.0,  
            help="Side Length b")
        ...
        pars.add_argument("--mode", default='3_sides', 
            help="Side Length c")

    def effect(self):
        tri = self.svg.get_current_layer()
        offset = self.svg.namedview.center
        self.options.s_a = self.svg.unittouu(
            str(self.options.s_a) + 'px')
        self.options.s_b = self.svg.unittouu(
            str(self.options.s_b) + 'px')
        self.options.s_c = self.svg.unittouu(
            str(self.options.s_c) + 'px')
        stroke_width = self.svg.unittouu('2px')

        if self.options.mode == '3_sides':
            s_a = self.options.s_a
            s_b = self.options.s_b
            s_c = self.options.s_c
            draw_tri_from_3_sides(s_a, s_b, s_c, 
                offset, stroke_width, tri)

        elif self.options.mode == 's_ab_a_c':
            ...
        ......

if __name__ == '__main__':
    Triangle().run()
```

The last two lines of the file is the main entry point.  The Python program 
initializes an instance of `Triangle` class and calls the `run` method. 
The `Triangle` class 
itself only defines two methods `add_argument` and `effect`, so the `run` method 
must be inherited from other classes. 

The `Triangle` class is inherited from `EffectExtension` class of `inkex` module.
The `inkex` Python module files are in the `inkex` directory. The `inkex` is 
the most basic module of Inkscape extension system. It is like a framework upon 
which we build our own extensions. 

Here is a list of directory names and file names under the `inkex` directory. 

<pre>
 (dir) deprecated-simple 
 (dir) elements  
 (dir) tester  
    33 ./__init__.py     # line of code | file name
   377 ./base.py
   425 ./bezier.py
   474 ./colors.py
   233 ./command.py
   403 ./deprecated.py
   378 ./extensions.py
    50 ./inkscape_env.py
   214 ./inx.py
    66 ./localization.py
  1672 ./paths.py
   100 ./ports.py
   382 ./styles.py
  1116 ./transforms.py
   120 ./turtle.py
    76 ./tween.py
   107 ./units.py
   209 ./utils.py
  6435 total

     3 directories, 18 files
</pre>

The `EffectExtension` class is defined in the `extensions.py` file, but it's just 
a subclass of `SvgThroughMixin` and `InkscapeExtension`. Pay attention to the docstring 
of the class, it summarizes what this class does. 

```python
class EffectExtension(SvgThroughMixin, InkscapeExtension):
    """
    Takes the SVG from Inkscape, modifies the selection or the document
    and returns an SVG to Inkscape.
    """
    pass
```

The `SvgThroughMixin` and `InkscapeExtension` classes are defined in the `base.py` 
file. The `run` method is defined in `InkscapeExtension` class. The code is shown 
below. 

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

## Logging Experiment

Let's add some logging code to this file and see logging output. If you are not 
family with Python logging module, take a quick look at the 
[Python Logging Howto Page](https://docs.python.org/3/howto/logging.html). This 
15 minutes [youtube video](https://youtu.be/-ARI4Cz-awo) 
explains the basics of logging very well. 

In order to 
modify files in the system extenson directory, we need to change the directory and 
file permissions.  Run those bash commands when you are in the `system extension` 
directory. Be sure to make a copy of the directory before modifying files. 

```
$ cd /usr/share/inkscape/extensions
$ sudo chmod -R 777 ../extensions/
```

If you install inkscape via `snap`, you will have a difficult time modidfying any 
files under `/snap` directory.  This is a security feature of snap apps. 

Add those lines at the top of `base.py` to setup logging module.

```python
 from .localization import localize
 
 # setup logging
 import logging
 logging.basicConfig(filename = 
     '/home/george/Desktop/new-logging.txt', filemode='w', 
     format='%(levelname)s: %(message)s', level=logging.DEBUG)
```

Then add six logging debug output lines in the `run` method. 

```python
def run(self, args=None, output=stdout):
    # type: (Optional[List[str]], Union[str, IO]) -> None
    """Main entrypoint for any Inkscape Extension"""
    logging.debug('run starts')    ##1
    logging.debug(f'python exec: {sys.executable}') ##2

    try:
        if args is None:
            args = sys.argv[1:]
        self.parse_arguments(args)

        if self.options.input_file is None:
            self.options.input_file = sys.stdin

        if self.options.output is None:
            self.options.output = output

        logging.debug(f'sys argv: {sys.argv}') ##3
        logging.debug(f'input : {self.options.input_file}') ##4
        logging.debug(f'output : {self.options.output}') ##5

        self.load_raw()
        self.save_raw(self.effect())

    except AbortExtension as err:
        err.write()
        sys.exit(ABORT_STATUS)

    finally:
        self.clean_up()
    logging.debug('run ends')  ##6
```

The results of logging in the `new-loggin.txt` file are

```
DEBUG: run starts
DEBUG: python exec: /usr/bin/python3
DEBUG: sys argv: ['triangle.py', '--s_a=100', '--s_b=100', 
   '--s_c=100', '--a_a=60', '--a_b=30', '--a_c=90', 
   '--mode=3_sides', '/tmp/ink_ext_XXXXXX.svgVYXM70']
DEBUG: input : /tmp/ink_ext_XXXXXX.svgVYXM70
DEBUG: output : <_io.BufferedWriter name='<stdout>'>
DEBUG: run ends
```

Between the `load_raw` and `save_raw` method calls, there is an `effect` method call. 
The `effect` method is defined in the `InkscapeExtension` class, but it raises an 
`NotImplementedError` exception.  The method is a placeholder for subclasses to override.  
The `effect` method in `Triangle` class overrides it. 

If you install inkscape via `snap`, you will have a difficult time to modidfy any 
files under `/snap` directory.  How do I know it? I waste 3 hours trying 
various methods and it turns out to be a security feature of snap apps. 

The `InkscapeExtension` class defines a `debug` method. We can invoke this method 
to output messages. The method redirects a message to the stardard error stream,  
and Inkscape will display the message on a dialog box. However, the logging 
module is more flexible to use than this method. 

## What's Next

You may feel overwhelmed or even frustrated by now if you are not very familar 
with Python. Most Python introductory books do not even discuss classes. But keep 
reading and experimenting, and the code will gradually start making sense to you. 

Like most things in the programming world, it's better to learn something and 
start working. There may be things that you don't understand, but you shouldn't 
wait to start because you probably will never understand everything. 
The extension Python code is all open source and available to you. You are free 
to experiment and modify as you like. 



**Next section we will take another look at `triangle.py` and start a skeleton 
extension. **  



