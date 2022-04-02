title: Inkex Module As API
slug: inkex_module
date: 2022-03-28 09:26
category: extension
chapter: 17
note: Inkex Module

## Inkex Module

Many Inkscape extensions load an SVG file from Inkscape, add some elements 
on the drawing, and transmit the modified SVG back to Inkscape. For example, 
the `Hello` extension discussed in Chapter 5 adds a message on a drawing.

At some point, someone may ask you the question "Can we run the program without 
Inkscape? I want to run it as a Python program". The answer is "Yes, 
definitely".  This article discusses how to do that. 

In Ubuntu, the *system extension* directory is,

```
/usr/share/inkscape/extensions
```

The `inkex` module files are located in the `inkex` subdirectory. We can treat 
the module as an API (Application Programming Interface) or a graphics library. 

## Load Inkex

As we discussed in Chapter 2, the Inkscape invokes Python complier at this 
location (see below) to run extension programs. The `inkex` module depends on the `lxml` 
module, which is already installed for this compiler. 

```
/usr/bin/python3
```

We also need to let the compiler know how to find the `system extension` directory and 
`user extension` directory. This is handled by modifying the system environment 
variable `PYTHONPATH`. In Bash terminal, type `export` command to set the variable. 

```
$export PYTHONPATH=${PYTHONPATH}:/usr/share/inkscape/extensions:\
> /home/george/.config/inkscape/extensions  

$echo $PYTHONPATH
:/usr/share/inkscape/extensions:/home/george/......

$/usr/bin/python3
Python 3.9.7 (default, Sep 10 2021, 14:59:43) 
[GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import inkex
>>> import hello
>>> exit()

$/usr/bin/python3 hello_app.py  # see below for hello_app.py
```

We can also add the export statement to the `.bashrc` file under 
Ubuntu user directory. Or create a short Bash script to setup the `PYTHONPATH`
environment variable and run the Python script. 

## Python Script

Let's create a Python script `hello_app.py` to run the code in the `Hello` extension 
discussed in Chapter 5. The `Hello` extension program uses the `ArgParse` module 
to parse the arguments.  We create a `Param` class to simulate `ArgParse` 
arguments, and override the `parse_arguments` method to assign a `Param` object 
to `self.options` variable. 

The `run` method derived from `EffectExtension` class accepts two optional 
arguments, `args` and `output` (see Chapter 3).  The `args` argument must have 
two instance variables `input_file` and `output`.  The `input_file` can be either 
a stream or a file name. The `output` instance variable override the `output` 
argument of `run` method. In the example below, the `blank_svg` is a string 
representing a blank SVG file in Inkscape. 

The script below will create a `test.svg` in the same 
directory of `hello_app.py` file. The `run` method will invoke the `effect` 
method in `Hello` class defined in `hello.py`. Notice We are running the program 
outside of Inkscape. You do not need Inkscape installed to run 
this Python program.  

```py
# hello_app.py
import os
from hello import Hello


class HelloApp(Hello):
    def parse_arguments(self, args):
        self.options = args
        self.options.ids = []
        self.options.selected_nodes = []


class Param:
    def __init__(self):
        self.name = 'Inkex App'
	      ## add other GUI variables here
        

blank_svg = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg5"
   inkscape:version="1.1.1 (1:1.1+202109281954+c3084ef5ed)"
   sodipodi:docname="drawing.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="0.64052329"
     inkscape:cx="397.33138"
     inkscape:cy="561.25984"
     inkscape:window-width="2560"
     inkscape:window-height="1480"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" />
  <defs
     id="defs2" />
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1" />
</svg>'''


if __name__ == '__main__':
    h = HelloApp()
    args = Param()
    args.input_file = blank_svg.encode('utf-8') # or file name
    args.output = 'test.svg'
    h.run(args)
```

## Others 

We can also create a virtual environment with system Python compiler, 
and install `lxml` and other modules in the virtual environment.  This is 
the preferred way to work on this type of project.   

```
$python -m venv venv
$source venv/bin/activate
$pip install lxml    ## and other modules
```
