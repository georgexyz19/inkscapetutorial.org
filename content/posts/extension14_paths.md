title: Paths
slug: paths
date: 2021-08-25 14:42
category: extension
chapter: 14
note: Paths

## PathElement Class

The `PathElement` class represents a path element on a drawing.  The class is defined in 
the `inkex/elements/_polygons.py` module. It is derived from `PathElementBase` class. 
Both classes only include a few methods and properties. The Python interpreter session 
below shows how to get hold of a path element and invoke its methods and properties. 

The same drawing `drawing-21.svg` discussed in Chapter 9 is used here as an example. 
The path element is a typical Bezier curve with two end points and two control points. 

```
george@Inspiron-5515:~$ /usr/bin/python3
Python 3.9.5 (default, May 11 2021, 08:20:37) 
[GCC 10.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> import sys
>>> sys.path.append('/usr/share/inkscape/extensions')
>>> 
>>> from inkex import load_svg
>>> et = load_svg('/home/george/Desktop/drawing-21.svg')
>>> svg = et.getroot()
>>> 
>>> for el in svg:
...   print(el)
... 
namedview
defs
g
>>> 
>>> gel  = svg[-1]
>>> gel
<Element {http://www.w3.org/2000/svg}g at 0x7fc6ecd069a0>
>>> 
>>> for el in gel:
...   print(el)
... 
rect
ellipse
path
path
>>> 
>>> pel = gel[-1]
>>> 
>>> pel
<Element {http://www.w3.org/2000/svg}path at 0x7fc6ecd06b30>
>>> 
>>> pel.original_path
[Move(80.3412, 87.9089), Curve(99.575, 67.2665, 
    103.398, 73.9063, 113.129, 83.6942)]
>>> 
>>> pel.path  # defined in ShapeElement
[Move(80.3412, 87.9089), Curve(99.575, 67.2665, 
    103.398, 73.9063, 113.129, 83.6942)]
>>> 
>>> pel.__class__
<class 'inkex.elements._polygons.PathElement'>
>>> 
>>> pel.get_path()
'M 80.341223,87.908862 C 99.574968,67.266473 
    103.39751,73.906308 113.12895,83.694219'
>>> 
>>> pel.get('d')
'M 80.341223,87.908862 C 99.574968,67.266473 
    103.39751,73.906308 113.12895,83.694219'
>>> 
>>> 
```

## Path Class

The `path` property defined in `ShapeElement` class returns a `Path` object. 
Other classes derived from `ShapeElement` also have this `path` property. 

The `Path` class is defined in `inkex/paths.py` module. The `Path` object is 
interesting, and it is a list of other class objects. The `inkex/paths.py` module 
defines many other classes such as `Move`, `move`, `Horz`, `horz`, `Curve`, 
`curve` etc.

```
>>> p = pel.path
>>> p
[Move(80.3412, 87.9089), Curve(99.575, 67.2665, 
        103.398, 73.9063, 113.129, 83.6942)]
>>> p.bounding_box()
BoundingBox((80.341223, 113.12895),(74.37224453581157, 87.908862))
>>> 
>>> for pt in p.control_points:
...   print(pt)
... 
80.3412, 87.9089
99.575, 67.2665
103.398, 73.9063
113.129, 83.6942
>>> 
>>> for pt in p.end_points:
...   print(pt)
... 
80.3412, 87.9089
113.129, 83.6942
>>> 
>>> 
>>> p.reverse()
[Move(113.129, 83.6942), Curve(103.398, 73.9063, 
        99.575, 67.2665, 80.3412, 87.9089)]
>>> 
>>> from inkex import Transform
>>> p.transform(Transform('translate(10,10)'))  # return changed value
[Move(90.3412, 97.9089), Curve(109.575, 77.2665, 
        113.398, 83.9063, 123.129, 93.6942)]
>>> 
>>> p.to_absolute()
[Move(80.3412, 87.9089), Curve(99.575, 67.2665, 
        103.398, 73.9063, 113.129, 83.6942)]
>>> 
>>> str(p)
'M 80.3412 87.9089 C 99.575 67.2665 103.398 73.9063 113.129 83.6942'
>>> 
>>> p_str = str(p)
>>> from inkex import Path
>>> p_new = Path(p_str)
>>> p_new
[Move(80.3412, 87.9089), Curve(99.575, 67.2665, 
        103.398, 73.9063, 113.129, 83.6942)]
>>> p_new.__str__()
'M 80.3412 87.9089 C 99.575 67.2665 103.398 73.9063 113.129 83.6942'
>>> 
>>> m = p_new[0]
>>> m
Move(80.3412, 87.9089)
>>> m.args
(80.3412, 87.9089)
>>> 
>>> m.x = 80
>>> m.y = 88
>>> m
Move(80, 88)

```

It is easy to create a `Path` element from composing class objects. 
Here is an example to create a similar Bezier curve as shown above and 
add it to a drawing in memory.

```
>>> from inkex.paths import Move, Curve
>>> p2 = Path()
>>> m = Move(90, 90)
>>> p2.append(m)
>>> c = Curve(99, 67, 104, 74, 114, 84)
>>> p2.append(c)

>>> p2
[Move(90, 90), Curve(99, 67, 104, 74, 114, 84)]
>>>  
>>> from inkex import PathElement
>>> pel = PathElement.new(p2)
>>> pel
<Element {http://www.w3.org/2000/svg}path at 0x7fc6ecd06e50>
>>> gel
<Element {http://www.w3.org/2000/svg}g at 0x7fc6ecd069a0>

>>> gel.append(pel)
>>> for el in gel:
...   print(el)
... 
rect
ellipse
path
path
path  # new path element

```

## Path Related Extensions

Inkscape comes with many path related system extensions. They are listed under `Modify Path`, 
`Generate From Path`, and `Visualize Path` submenus under `Extensions` menu. 
Let's examine one of them and discuss its code. 

When we work on engineering drawings, the dimension tool is indispensable. The `Dimensions` 
menu under `Visualize Path` is such a tool. We can select several path elements or a single 
element and apply the extension. The extension will draw the auxiliary lines and two 
dimension lines with arrow heads. However, the tool does not automatically add dimension 
texts along the lines.  The figure below shows an example. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext14/dimensions.svg" alt="dimensions"> 
</div>

The `Dimensions` extension code is in the `dimension.inx` and `dimension.py` files under 
system extension directory. The `Dimension` class is derived from `PathModifier` class 
in `pathmodifier.py` module, which is in turn derived from `EffectExtension` class. 
The `Dimension` class doesn't use any methods in `PathModifier` class, so it is the 
same as subclassing `EffectExtension` class directly. 

The `Dimension` class defines 5 methods. We have discussed `add_arguments` and `effect` 
methods in previous chapters.  The other three methods `add_marker`, `horz_line`, 
`vert_line` are easy to understand. 

