title: Units and Coordinate Systems
slug: units-and-coordinate-systems
date: 2021-08-07 23:18
category: extension
chapter: 10
note: Units

## Extension Units

Inkscape extension [documentation page](https://inkscape.gitlab.io/extensions/documentation/index.html) has a [units](https://inkscape.gitlab.io/extensions/documentation/units.html) 
page. Inkscape units themselves are not complicated, and the difficult part is how 
Inkscape projects units in user coordinate system to viewport coordinate system. 

Most common units in Inkscape are pixel, point, millimeter, and inch. The `inkex/units.py` 
module defines a `CONVERSIONS` dictionary.  The base unit is `pixel` or `px`.  The dictionary 
value is the converting factor from other unit to `px`. For example, 1 `in` equals 96.0 `px`, 
and 1 `point` or `pt` equals 1.3333 `px`.  

```python
# a dictionary of unit to user unit conversion factors
CONVERSIONS = {
    'in': 96.0,
    'pt': 1.3333333333333333,
    'px': 1.0,
    'mm': 3.779527559055118,
    'cm': 37.79527559055118,
    'm': 3779.527559055118,
    'km': 3779527.559055118,
    'Q': 0.94488188976378,
    'pc': 16.0,
    'yd': 3456.0,
    'ft': 1152.0,
    '': 1.0,  # Default px
}
```

When we are working on a drawing, we often use different units to describe different elements. 
We describe the line stroke width as `1px` or `2px`, line length as `20mm` or `1.5in`, 
font size as `12pt` or `10pt`, 
paper size as `letter` (8.5in x 11in) in the US, or A4 (210mm x 297mm). 

The `1px` 
stroke width is an commonly picked number. If we want narrower width, `0.75px` is a good choice. 
We can choose `1.5px` or `2px` width when we need a bolder line. Microsoft Word default 
font is `11pt` Calibri, and it was `12pt` *Times New Roman* in earlier versions. An `10pt` 
font size is still considered legible when printed on paper, and smaller font size is 
often considered too tiny to read. 

## Coordinate Systems

When we create a `Line` element and add it to the drawing, we usually do not need to specify 
a unit for line length.  For example, here is the code for `el11` in previous chapter. 

```python
el1 = Line()
el1.set('x1', '10')
el1.set('y1', '10')
el1.set('x2', '40')
el1.set('y2', '40')
el1.set('style', self.style)
```

We do not need to specify the units for the SVG file either. The default `A4` page SVG 
file has those lines. 

```xml
<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"

```

What do those numbers mean?  The width and height attributes of svg tag mean the Inkscape 
canvas size. It is also called *viewport coordinate system*. It is on the right hand side of the 
following drawing. The default size 210mm x 297mm is the same size of a piece of A4 page. When 
we export the drawing to an PDF file, it will have the same size. If we print the PDF file 
on a piece of A4 paper, it is supposed to be 100% of the PDF. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext10/viewport.svg" alt="viewport"> 
</div>

When we create a line from (10, 10) to (40, 40), the coordinates are in the *user coordinate system* or 
*user space*. It is on the left hand size of the above drawing. 
The user coordinate system origin and size are defined as the `viewBox` attribute of `svg` 
tag. The `viewBox` attribue values (0 0 210 297) also do not have units. 

What are the units of those 
values? The svg specification says that the default user space unit is `pixel`. 
If we set the line start point 
as (10px, 10px) and end point as (40px, 40px) the result will be the same. However, the line will 
show up on the canvas as from (10mm, 10mm) to (40mm, 40mm) because line is mapped from user coordinate 
system to viewport coordinate system. This is confusing here.  We set the coordinates 
in pixel, but they show up on canvas in `mm`. So it is better to leave the units out. 

```python
el1.set('x1', '10px') # same as `10`
el1.set('y1', '10px') # prefer no unit
el1.set('x2', '40px')
el1.set('y2', '40px')
```

If we set the line from (10mm, 10mm) to (40mm, 40mm), it will be the same as set the coordinates 
from (37.795, 37.995) to (151.18, 151.18) in the user space.  Inkscape will automatically convert 
those numbers to pixels. 

## Unit Conversion

What if we know the size of an element on canvas, what value should we set in user space?
For example, we want a line with a stroke width of `1px`, what value should we set for 
the `stroke-width` attribute? The stroke width of `1px` is the same as `1/3.7795 = 0.2646mm`. 
When we set the `stroke-width` value as `0.2646`, it will show up as `1px` width on canvas.

We can also call `unittouu` method (property) of `BaseElement` class to do the conversion 
for us. It will convert a value in viewport coordinate system to user space. This covers 
most of what we need to know about Inkscape units and coordinate system mapping. 

```python
sw = self.svg.unittouu('1px') # sw is .2645...
```

If we want `10pt` font size text, we set the font-size to the below value. This is a more natural 
way to describe element sizes. 

```python
fz = self.svg.unittouu('10pt') # fz value is 3.5278
```

You may find coordinate mapping confusing if you do 
not have prior experiences on computer graphics system. The Inkscape 1.0 changes the 
y-axle of the viewport coordinate system to increase fom top to bottom, and origin to the 
top left corner. Before Inkscape 1.0, the origin is at the bottom left corner. You can 
imagine that the coordinate systems are even more confusing then. 

## Units Module 

The `inkex/units.py` Python module is independent of other modules, so it's easy to 
understand code in this module. Let's experiment the module in Python interpreter. 
Start the python interpreter with `/usr/bin/python3` command if the system has multiple python 
versions installed.  This is the system Python with `lxml` module installed. 

```
george@Inspiron-5515:~$ /usr/bin/python3
Python 3.9.5 (default, May 11 2021, 08:20:37) 
[GCC 10.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
```

If we simply import `inkex`, the interpreter can't find where the module is located. 
We can add the path to the `sys.path`.  

```python
>>> import inkex
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'inkex'

>>> import sys
>>> sys.path.append('/usr/share/inkscape/extensions')

>>> import inkex
>>> dir(inkex.units)
[...]
>>> help(inkex.units)
```


The `help(inkex.units)` command will show the functions defined in the module and 
a short description for each function. 

* `are_near_relative(point_a, point_b, eps=0.01)`  
    Return true if the points are near to eps

* `convert_unit(value, to_unit, default='px')`  
    Returns user units given a string representation of units in another system

* `discover_unit(value, viewbox, default='px')`  
    Attempt to detect the unit being used based on the viewbox

* `parse_unit(value, default_unit='px', default_value=None)`  
    Takes a value such as 55.32px and returns (55.32, 'px')  
    Returns default (None) if no match can be found

* `render_unit(value, unit)`  
    Checks and then renders a number with its unit

It is nice to have source code available. But it is easier for us to understand 
how to use those functions through examples.  We can `grep` the Inkscape system 
extensions to find out how they are used.  

```python
>>> from inkex import units
>>> p = units.parse_unit('55.32px')
>>> p
(55.32, 'px')

>>> p = units.parse_unit('55.32pt')
>>> p
(55.32, 'pt')

>>> p = units.parse_unit('55.32bt')
>>> p # returns None

>>> p = units.parse_unit('55.32')
>>> p
(55.32, 'px') # default unit is pixel

>>> units.are_near_relative(0.123, 0.121)
False
>>> units.are_near_relative(0.123, 0.122)
True
>>> units.are_near_relative(0.1234, 0.1232)
True

>>> units.discover_unit('210mm', 210, default='px')
'mm'
>>> units.discover_unit('8.5in', 210, default='px')
'px'  # default
>>> units.discover_unit('8.5in', 215.9, default='px')
'mm'  # letter size

>>> units.convert_unit('8.5in', 'mm')
215.9

>>> units.render_unit(10, 'in')
'10in'

>>> units.convert_unit('8.5', 'mm')
2.2489583333333334
>>> units.convert_unit('1px', 'mm')
0.26458333333333334
>>> units.convert_unit('10pt', 'mm')
3.5277777777777777
```