title: Element Classes
slug: element-classes
date: 2021-08-04 13:27
category: extension
chapter: 8
note: Element Classes

## Custom Element Classes

The `inkex` module defines many custom element classes. The Python files are under the 
`inkex/elements` directory and module names all start with an underscore `_`. It indicates 
that those are internal modules and we should not directly import those modules in 
our user extensions. 

Usually when we load an XML file into memory, we use the default XML parser that comes with 
`lxml` module. 

```
doc = etree.parse('test.xml')
```

Or you can invoke the `etree.XMLParser` method to create a parser and pass the parser object to 
`etree.parse` method. The `huge_tree` option shown below "disables security restrictions 
and supports deep trees and long text content". 

```
p = etree.XMLParser(huge_tree=True)
doc = etree.parse('test.xml', parser=p)
```

The `lxml` documentation has a page regarding 
[using custom Element classes in lxml](https://lxml.de/element_classes.html). On the 
"Tree based element class lookup in Python" section, it has example code like this. 

```
class MyLookup(etree.PythonElementClassLookup):
    def lookup(self, document, element):
        return MyElementClass 

parser = etree.XMLParser()
parser.set_element_class_lookup(MyLookup())

```

The `MyLookup` class must have a method `lookup` as shown above. The `document` argument 
of the `lookup` method acts like `self.document` object and the `element` argument 
acts like an `Element` object. The return value `MyElementClass` is a custom class 
defined elsewhere which must inherit from `etree.ElementBase` class. 

The code in the `elements/_base.py` module follows the above example to define the lookup 
class `NodeBasedLookup`. It creates a custom parser `SVG_PARSER` and define the `load_svg` 
method which uses the parser. 

The `inkex` module authors did the hard work of writing custom Element classes.  It currently 
has 64 classes included in Inkscape 1.1 release. Here are a few examples. 

```
inkex.elements._meta.Defs
inkex.elements._meta.StyleElement
inkex.elements._svg.SvgDocumentElement
inkex.elements._groups.Layer
inkex.elements._polygons.PathElement
inkex.elements._polygons.Polyline
inkex.elements._polygons.Polygon
inkex.elements._polygons.Line
inkex.elements._polygons.Rectangle
inkex.elements._polygons.Circle
......
```

Let's take a look at the `PathElement` inheritance tree. The class is derived from `ShapeElement` 
which in turn is derived from `BaseElement` class. 

<pre>
etree.ElementBase
  BaseElement
    ShapeElement
      PathElement
</pre>

With the parser in place, the return value from `etree.parse` method will contain `Rectangle` 
class object instead of general `Element` class object.  This is a simplification, and it 
actually is a Python proxy object because `lxml.etree` is based on libxml2, which loads 
the XML tree into memory in a C structure. 

## Add New Elements

The code in the `Hello` extension is the typical way to add new elements to a drawing. We 
create an element object first, set some attributes, and add the element to a
containing group or layer. The new element will become part of the drawing. 

```python
def effect(self):
    name = 'Hello ' + self.options.name 
    layer = self.svg.get_current_layer()
    layer.add(self.add_text(10, 10, name))

def add_text(self, x, y, text):
    """Add a text label at the given location"""
    elem = TextElement(x=str(x), y=str(y))
    elem.text = text
    elem.style = {
        'font-size': self.svg.unittouu('30px'),
        'fill-opacity': '1.0',
        'stroke': 'none',
        'font-weight': 'normal',
        'font-style': 'normal' }
    return elem
```




## References







