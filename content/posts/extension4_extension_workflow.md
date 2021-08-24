title: Extensions Workflow
slug: extension-workflow
date: 2021-07-28 08:42
category: extension
chapter: 4
note: extension workflow

We will discuss those two line of code in `run` method of `InksacpeExtension` 
class in this chapter. 

```
self.load_raw()
self.save_raw(self.effect())
```

## Load

The code of `load_raw` method of `InkscapeExtension` class is shown below. 

```python
def load_raw(self):
    # type: () -> None
    """Load the input stream or filename, save everything to self"""
    if isinstance(self.options.input_file, str):
        self.file_io = open(self.options.input_file, 'rb')
        document = self.load(self.file_io)
    else:
        document = self.load(self.options.input_file)
    self.document = document
```

We know the value of `self.options.input_file` is a string from last chapter, 
so the if part of the `if...else...` statement will execute. It calls the 
`open` method to create a file object, and pass it to the `self.load` method. 
The `self.load` method defined in the `SvgInputMixin` class is invoked here.
Below is the code of the `load` method of `SvgInputMixin` class. 

```python
def load(self, stream):
    # type: (IO) -> etree
    """Load the stream as an svg xml etree and make a backup"""

    document = load_svg(stream)
    self.original_document = copy.deepcopy(document)
    self.svg = document.getroot()
    self.svg.selection.set(*self.options.ids)
    if not self.svg.selection and self.select_all:
        self.svg.selection = 
            self.svg.descendants().filter(*self.select_all)
    
    return document
```
The `load` method in turn calls a function `load_svg` imported from another module. 
It also adds two new instance variable `original_document` and `svg`. 

```python
from .elements._base import load_svg, BaseElement
```

Here is the function `load_svg` definition in the `inkex/elements/_base.py` module. 

```python
from lxml import etree
......

SVG_PARSER = etree.XMLParser(huge_tree=True, strip_cdata=False)
SVG_PARSER.set_element_class_lookup(NodeBasedLookup())

def load_svg(stream):
    """Load SVG file using the SVG_PARSER"""
    if (isinstance(stream, str) and 
        stream.lstrip().startswith('<'))\
      or (isinstance(stream, bytes) and 
            stream.lstrip().startswith(b'<')):
        return etree.ElementTree(etree.fromstring(stream, 
                                parser=SVG_PARSER))
    return etree.parse(stream, parser=SVG_PARSER)

```

Here the last statemetn `return etree.parse(...)` is executed because `steam` 
is a file object, not a string or bytes type. The `etree.parse` method in `lxml` 
module does the actual loading work. The `lxml` module is not in the standard 
library, and it is a third part library. It will be automatically installed 
when we install Inkscape. We will discuss `lxml` module later. 

## Modify

The `Triangle` object has two instance variables `document` and `svg`, and both
reference the same XML tree in memory. We can modify the XML tree via either of 
those two variables. It also saves a copy 
of `document` in `original_document` instance variable. 

The actual modification happens in the `effect` method of `Triangle` class thru the `svg` instance variable. 

```python
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
        draw_tri_from_3_sides(s_a, s_b, s_c, offset, 
                stroke_width, tri)
    ......
```

The first line of the method calls `get_current_layer` method of `svg` object
to get an object representing current layer. The current layer information is saved in 
the SVG file itself.  The second line get the Inkscape view center coordinates. 
The next four lines of code convert number unit from pixel to SVG internal default unit 
millimeter.  For example, the `s_a` value is 100 px before the coversion, and 
the value is 26.45 mm after.  In Inkscape 1 inch is 96 pixels, and 1 inch is 25.4 mm.
So the conversion is 100/96 in * 25.4 = 26.45 mm.

The `effect` method calls `draw_tri_from_3_sides` function defined earlier in the 
module. The function in turn calls the `draw_SVG_tri` function to create an 
`inkex.PathElement` element and add it to the layer. We will discuss the 
`PathElement` and other SVG elements later. 

```python
def draw_SVG_tri(point1, point2, point3, offset, width, name, parent):
    style = {'stroke': '#000000', 'stroke-width': str(width), 
            'fill': 'none'}
    elem = parent.add(inkex.PathElement())
    elem.update(**{
        'style': style,
        'inkscape:label': name,
         'd': 'M ' + str(point1[X] + offset[X]) + ',' + 
                    str(point1[Y] + offset[Y]) +
              ' L ' + str(point2[X] + offset[X]) + ',' + 
                    str(point2[Y] + offset[Y]) +
              ' L ' + str(point3[X] + offset[X]) + ',' + 
                    str(point3[Y] + offset[Y]) +
              ' L ' + str(point1[X] + offset[X]) + ',' + 
                    str(point1[Y] + offset[Y]) + ' z'})
    return elem

.....

def draw_tri_from_3_sides(s_a, s_b, s_c, offset, width, parent):  
    # draw a triangle from three sides (with a given offset
    if is_valid_tri_from_sides(s_a, s_b, s_c):
        a_b = angle_from_3_sides(s_a, s_c, s_b)

        a = (0, 0)  # a is the origin
        b = v_add(a, (s_c, 0))  #point B is horizontal from origin
        c = v_add(b, pt_on_circ(s_a, pi - a_b))  # get point c
        c[1] = -c[1]

        offx = max(b[0], c[0]) / 2  
        # b or c could be the furthest right
        offy = c[1] / 2  # c is the highest point
        offset = (offset[0] - offx, offset[1] - offy)  
        # add the centre of the triangle to the offset

        draw_SVG_tri(a, b, c, offset, width, 'Triangle', parent)
    else:
        inkex.errormsg('Invalid Triangle Specifications.')

```

## Save

This section discusses the third method call `self.save_raw` shown at the beginning 
of this chapter. The `save_raw` method is defined in `InkscapeExtension` class like 
this. 

```python
def save_raw(self, ret):
    # type: (Any) -> None
    """Save to the output stream, use everything from self"""
    if self.has_changed(ret):
        if isinstance(self.options.output, str):
            with open(self.options.output, 'wb') as stream:
                self.save(stream)
        else:
            self.save(self.options.output)
```

The method tests if the SVG file has changed via the `has_changed` method in 
`SvgThroughMixin` class. It converts the `original_document` and `document` 
objects to string and compares if they are the same. 

The `save_raw` method then calls the `save` method defined in `SvgOutputMixin`
class. The code of `save` method is shown below. It calls the `write` method 
of output stream to transmit the modified SVG back to Inkscape. 

```python
def save(self, stream):
    # type: (IO) -> None
    """Save the svg document to the given stream"""
    if isinstance(self.document, (bytes, str)):
        document = self.document
    elif 'Element' in type(self.document).__name__:
        # isinstance can't be used here because etree is broken
        doc = cast(etree, self.document)
        document = doc.getroot().tostring()
        # actually execute this part
    else:
        raise ValueError(f"Unknown type of document: 
            {type(self.document).__name__} can not save.")

    try:
        stream.write(document)
    except TypeError:
        # we hope that this happens only when 
           # document needs to be encoded
        stream.write(document.encode('utf-8')) # type: ignore
```

## Python Module lxml

When we develop an Inkscape extension, we don't need to care too much about 
load and save processes. The `inkex` module already has code to handle
them. It actually warps around a third party python module `lxml`, which 
does the actualy XML loading, parsing, and saving.  The 
[lxml official website](https://lxml.de/) 
has lots of useful information. We will also discuss this module in later chapters. 


