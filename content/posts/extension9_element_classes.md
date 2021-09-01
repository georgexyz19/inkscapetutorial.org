title: Inkex Element Classes
slug: inkex-element-classes
date: 2021-08-24 10:54
category: extension
chapter: 9
note: Element Classes

All element classes like `Polyline` and `TextElement` are directly or indirectly derived from 
`BaseElement` class, which is define in the `inkex/elements/_base.py` module. The 
`BaseElement` class is subclassed from `etree.ElementBase` class.  The `etree.ElementBase` 
class is described as "public Element class" in its 
[documentation page](https://lxml.de/api/lxml.etree.ElementBase-class.html). 

The `BaseElement` defines an `__init_subclass__` magic method which will register all 
its subclasses and add them to a `lookup_table` defined in `NodeBasedLookup` class. When 
the XML parser starts parsing a document, it will use this `lookup_table` 
to find appropriate custom element class for each element. It probably can be implemented 
as a class decorator in Python, but every `BaseElement` subclasses need to be decorated 
with the decorator.  

```
class BaseElement(etree.ElementBase):
    """Provide automatic namespaces to all calls"""
    def __init_subclass__(cls):
        if cls.tag_name:
            NodeBasedLookup.register_class(cls)
```
Here is a class hierarchy diagram for some element classes. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext14/elemclasses.svg" alt="elem classes"> 
</div>

## SvgDocumentElement Class

When we load an SVG document into memory with inkex module, the root element is an 
`SvgDocumentElement` class object. Let's draw some shapes on canvas, save the SVG 
file, and load it. The drawing has 4 simple elements as shown below. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext9/drawing.svg" alt="a drawing"> 
</div>

The `load_svg` function is defined in the `inkex/elements/_base.py` module. The 
function invokes `etree.parse` method to load the SVG file. The return value is 
an `ElementTree` object. As discussed in the last chapter, we can call the 
`getroot` method to get a top level `Element` object, which is the `svg` tag 
element. The `svg` tag element is actually of type `SvgDocumentElement`, which 
is subclass of `etree._Element` class. 

```
george@Inspiron-5515:~$ /usr/bin/python3
Python 3.9.5 (default, May 11 2021, 08:20:37) 
[GCC 10.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> sys.path.append('/usr/share/inkscape/extensions')

>>> from inkex import load_svg
>>> et = load_svg('/home/george/Desktop/drawing-21.svg')
>>> et
<lxml.etree._ElementTree object at 0x7f3d0f71ca80>

>>> svg = et.getroot()
>>> svg.tag
'{http://www.w3.org/2000/svg}svg'
>>> svg.__class__
<class 'inkex.elements._svg.SvgDocumentElement'>

>>> from lxml import etree
>>> from inkex import BaseElement
>>> isinstance(svg, etree.ElementBase)
True
>>> isinstance(svg, etree._Element)
True
>>> issubclass(etree.ElementBase, etree._Element)
True
```

The `Element` class object is iterable.  When we loop through the object, 
we can print out child tag names. The four shape elements are nested inside 
the `g` layer object, and we can loop through the layer object to print 4 
element tag names. 

The interesting part of the results shown below is that all element nested 
inside the `svg` tag has an `svg` namespace unless it is specified with an explicit 
namespace such as `sodipodi:namedview`. 

```
>>> len(svg)
3
>>> for el in svg:
...   print(el.tag)
... 
{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview
{http://www.w3.org/2000/svg}defs
{http://www.w3.org/2000/svg}g

>>> gel = svg[-1] # group
>>> gel.tag
'{http://www.w3.org/2000/svg}g'
>>> len(gel)
4
>>> for el in gel:
...   print(el.tag)
... 
{http://www.w3.org/2000/svg}rect
{http://www.w3.org/2000/svg}ellipse
{http://www.w3.org/2000/svg}path
{http://www.w3.org/2000/svg}path

```

The `SvgDocumentElement` class is defined in the `inkex/elements/_svg.py` module. The 
class defines an `_init` method, which is called once during `Element` class instantiation 
time.  Other methods and properties are not hard to understand. Here are some examples.

```
>>> svg.get_ids()
{'svg5', 'rect31', 'path55', 'layer1', 'path159', 'path274', 'defs2', 'namedview7'}
>>> 
>>> svg.get_unique_id('rect31')
'rect318029'
>>> 
>>> svg.get_ids()
{'svg5', 'rect31', 'path55', 'layer1', 'path159', 'path274', 
    'rect318029', 'defs2', 'namedview7'}
>>> 
>>> svg. get_page_bbox()
BoundingBox((0, 210.0),(0, 297.0))
>>> 
>>> svg.get_current_layer()
<Element {http://www.w3.org/2000/svg}g at 0x7f3d0ccfabd0>
>>> 
>>> svg.getElementById('path55')
<Element {http://www.w3.org/2000/svg}ellipse at 0x7f3d0c0ebdb0>

>>> svg.getElementByName('Layer 1')
<Element {http://www.w3.org/2000/svg}g at 0x7f3d0ccfabd0>
>>> 
>>> svg.name
'drawing-21.svg'
>>> 
>>> svg.namedview
<Element {http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview
    at 0x7f3d0c0ebbd0>
>>> 
>>> svg.get_viewbox()
[0.0, 0.0, 210.0, 297.0]
>>> 
>>> svg.width
210.0
>>> svg.height
297.0
>>> svg.scale
1.0
>>> svg.unit
'mm'
>>> svg.stylesheets
[]
>>> svg.stylesheet
[]

```

## BaseElement Class

The `BaseElement` class is defined in the `inkex/elements/_base.py` module. All element 
classes derive from the `BaseElement` class, and the methods and properties are designed for 
different types of elements. The class defines a `WRAPPED_ATTRS` class variable, and a 
`wrapped_attrs` property, which returns a dictionary. 

```
>>> svg.wrapped_attrs
{'transform': ('transform', <class 'inkex.transforms.Transform'>), 
  'style': ('style', <class 'inkex.styles.Style'>), 
  'class': ('classes', <class 'inkex.styles.Classes'>)}
```

The `BaseElement` class defines `__setattr__` and `__getattr__` magic methods. They 
add supports for three nested attribute `transform`, `style`, and `class`. For example, 
we can assign a string value to the transform property. The `__setattr__` method 
will convert it to an `Transform` class object and assign it to the property. 

```
>>> rel = gel[0]
>>> rel.transform
Transform(((1, 0, 0), (0, 1, 0)))
>>> rel.transform ='translate(10, 10) rotate(30)'
>>> rel.transform
Transform(((0.866025, -0.5, 10), (0.5, 0.866025, 10)))
>>> rel.transform ='scale(2)'
>>> rel.transform
Transform(((2, 0, 0), (0, 2, 0)))
```

The `BaseElement` class also defines `set` and `get` methods.  Both methods add 
namespace support. When we set an attribute with a namespace like `inkscape:label`, 
the `set` method will convert the namespace `inkscape` to a long string `{http...}`. 
The `update` method calls `set` method to set attributes, and the `new` method 
calls `update` method. So both `new` and `update` methods supports nested attribute and 
namespace. The `pop` method deletes an existing attribute. 

```
>>> rel.set('inkscape:label', 'rectangle')
>>> rel.attrib
{'id': 'rect31', 'width': '43.4631', ...
   '{http://www.inkscape.org/namespaces/inkscape}label': 'rectangle'}

>>> rel.update(width='40', inkscape__label='rect1') # double underscore as sep
>>> rel.attrib
{'id': 'rect31', 'width': '40', ... 
  '{http://www.inkscape.org/namespaces/inkscape}label': 'rect1'}

>>> rel.pop('inkscape:label')
'rect1'
```

Other notable methods in the class are shown in the example code below. 

```python
>>> from inkex import Group
>>> gel_new = Group.new('newgroup')  # create a new group obj
>>> gel_new.tostring()
b'<g inkscape:label="newgroup"/>'

>>> gel.add(gel_new)
<Element {http://www.w3.org/2000/svg}g at 0x7f3d0ccfa630>

>>> for el in gel:
...   print(el.tag)
... 
{http://www.w3.org/2000/svg}rect
{http://www.w3.org/2000/svg}ellipse
{http://www.w3.org/2000/svg}path
{http://www.w3.org/2000/svg}path
{http://www.w3.org/2000/svg}g


>>> gel_new.set_random_id()
>>> gel_new.eid
'g1675'
>>> gel_new.get_id()
'g1675'

>>> gel_new.set_id('g1678')
>>> gel_new.eid
'g1678'

>>> gel_new.root
<Element {http://www.w3.org/2000/svg}svg at 0x7f3d0f7229a0>
>>> 
>>> gel.descendants()
ElementList([('/*/*[3]', 
      <Element {http://www.w3.org/2000/svg}g at 0x7f3d0ccfabd0>), 
    ('/*/*[3]/*[1]', 
      <Element {http://www.w3.org/2000/svg}rect at 0x7f3d0c0ebd60>), 
    ... )  

>>> gel_new.ancestors()
ElementList([('/*/*[3]', 
    <Element {http://www.w3.org/2000/svg}g at 0x7f3d0ccfabd0>), 
    ('/*', 
      <Element {http://www.w3.org/2000/svg}svg at 0x7f3d0f7229a0>)])

>>> svg.findone('g')  # return nothing
>>> svg.findone('svg:g')
<Element {http://www.w3.org/2000/svg}g at 0x7f3d0ccfabd0>


>>> svg.findone('//svg:rect')
<Element {http://www.w3.org/2000/svg}rect at 0x7f3d0c0ebd60>

>>> svg.findall('//svg:rect')   # not sure why error, a bug?
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/share/inkscape/extensions/inkex/elements/_base.py", 
      line 389, in findall
    return super().findall(pattern, namespaces=namespaces)
  File "src/lxml/etree.pyx", line 1558, in lxml.etree._Element.findall
  File "src/lxml/_elementpath.py", line 334, in lxml._elementpath.findall
  File "src/lxml/_elementpath.py", line 312, in lxml._elementpath.iterfind
  File "src/lxml/_elementpath.py", line 281, in 
    lxml._elementpath._build_path_iterator
SyntaxError: cannot use absolute path on element

>>> svg.xpath('//svg:rect')
[<Element {http://www.w3.org/2000/svg}rect at 0x7f3d0c0ebd60>]
>>> svg.xpath('//svg:path')
[<Element {http://www.w3.org/2000/svg}path at 0x7f3d0c0ebea0>, 
  <Element {http://www.w3.org/2000/svg}path at 0x7f3d0c0eb9f0>]


>>> gel_new.delete()
>>> for el in gel:
...   print(el.tag)
... 
{http://www.w3.org/2000/svg}rect
{http://www.w3.org/2000/svg}ellipse
{http://www.w3.org/2000/svg}path
{http://www.w3.org/2000/svg}path
>>> 
>>> gel[-1].replace_with(gel_new)

>>> for el in gel:
...   print(el.tag)
... 
{http://www.w3.org/2000/svg}rect
{http://www.w3.org/2000/svg}ellipse
{http://www.w3.org/2000/svg}path
{http://www.w3.org/2000/svg}g
>>> 

>>> str(svg)  # call __str__ method
'svg'
>>> 
>>> gel.add(gel_new.copy())
<Element {http://www.w3.org/2000/svg}g at 0x7f3d0c0ff400>
>>> 
>>> [str(el) for el in gel]  # this is a better way to see children
['rect', 'ellipse', 'path', 'g', 'g']
>>> 
>>> 
>>> gel_new.duplicate()
<Element {http://www.w3.org/2000/svg}g at 0x7f3d0c0ff450>
>>> 
>>> [str(el) for el in gel]
['rect', 'ellipse', 'path', 'g', 'g', 'g']

```

