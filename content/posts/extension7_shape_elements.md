title: Custom Shape Elements
slug: shape-classes
date: 2021-08-04 13:27
category: extension
chapter: 7
note: Shape Elements

## Custom Element Classes

The `inkex` module defines many custom element classes. The Python files are under the 
`inkex/elements` directory and module names all start with an underscore `_`. It indicates 
that those are internal modules and we should not directly import those modules. 
When `inkex` module loads an SVG file, it uses those custom 
element classes and returns objects of custom element class instead of generic 
`Element` class of `lxml`. 


The `inkex` module creators did the hard work of writing custom element classes.  It currently 
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

If an SVG file contains an `rect` shape element, it will become an `Rectangle` object in 
memory when `inkex` loads and parses the file.  When we write user extensions, we can 
create objects of those custom element classes, and add them to a containing 
element such as layer or group. 

Let's take a look at the `PathElement` inheritance tree. The class is derived from `ShapeElement` 
which in turn is derived from `BaseElement` class. 

<pre>
etree.ElementBase
  BaseElement
    ShapeElement
      PathElement
</pre>

## Create New Elements

The code in the `Hello` extension shows the typical way to add new elements to a drawing. We 
create an element object first, set some attributes, and add the element to a
containing group or layer. The new element will become part of the drawing. 

The example below shows how to add shape and text elements to a drawing. Here are the 
contents in the `newelement.inx` file.  

```xml
<?xml version="1.0" encoding="UTF-8"?>
<inkscape-extension 
  xmlns="http://www.inkscape.org/namespace/inkscape/extension">
    <name>New Element</name>
    <id>user.newelement</id>
    <effect>
        <object-type>all</object-type>
        <effects-menu>
            <submenu name="Custom"/>
        </effects-menu>
    </effect>
    <script>
        <command location="inx" interpreter="python">
          newelements.py</command>
    </script>
</inkscape-extension>
```

Save the following code in a `newelement.py` file under user extension directory. 

```python
import inkex
from inkex import Line, Polyline, Polygon, Rectangle, Circle,\
    Ellipse, PathElement
from inkex import TextElement


class NewElement(inkex.EffectExtension):

    def effect(self):
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : '0.264583'}
        self.text_template = \
            'font-size:%dpx;text-align:center;text-anchor:middle;'
        layer = self.svg.get_current_layer()
        layer.add(*self.add_line(), *self.add_rect())
        layer.add(self.add_circle(), self.add_ellipse(), 
            self.add_polygon(), self.add_path())
        layer.add(*self.add_coordinates())

    def add_line(self):
        el1 = Line()
        el1.set('x1', '10')
        el1.set('y1', '10')
        el1.set('x2', '40')
        el1.set('y2', '40')
        el1.set('style', self.style)

        el2 = Line.new(start=(40, 10), end=(10, 40))
        el2.style = self.style
        
        el3 = Line()
        el3.update(**{
            'x1': '50', 
            'y1': '10', 
            'x2': '80', 
            'y2': '40',
            'style': self.style
        })

        el4 = Line(x1='50', y1='40', x2='80', y2='10')
        el4.style = self.style

        return el1, el2, el3, el4

    def add_rect(self):
        el1 = Rectangle(x='10', y='60', width='30', height='20')
        el1.style = self.style

        el2 = Rectangle.new(50, 60, 30, 20)
        el2.style = self.style 
        return el1, el2

    def add_circle(self):
        el = Circle.new(center=(105, 25), radius=15)
        el.style = self.style
        return el

    def add_ellipse(self):
        el = Ellipse.new(center=(105, 70), radius=(15,10))
        el.style = self.style
        return el

    def add_polygon(self):
        el = Polygon()
        el.set('points', 
            '130,10 160,10 160,25 145,25 145,40 130,40')
        el.style = self.style
        return el 

    def add_path(self):
        el = PathElement()
        el.set('d', 'M 130,60 h30 v10 h-15 v10 h-15 z')
        el.style = self.style
        return el

    def add_text(self, x, y, position='top', font_size=3.88):
        text = TextElement()
        x0, y0 = x, y
        # adjust y position
        if position == 'top':
            y = y - 2
        elif position == 'bottom':
            y = y + 4
        else:
            y = y 
        text.set('x', x)
        text.set('y', y)
        text.set('style', self.text_template % font_size)
        text.set('xml:space', 'preserve')
        text.text = f'({x0},{y0})'
        return text
    
    def add_coordinates(self):
        coordinates = [ (10, 10), (40, 40, 'bottom'), 
                        (40, 10), (10, 40, 'bottom'),
                        (50, 10), (80, 40, 'bottom'), 
                        (50, 40, 'bottom'), (80, 10, 'top'),
                        (105, 25, 'top'), (105, 70, 'top'), 
                        (10, 60, 'top'), (50, 60, 'top'), 
                        (130, 10, 'top'), (130, 60, 'top'),
                        (160, 10, 'top'), (160, 60, 'top'),
                    ]

        text_elements = [self.add_text(*c) for c in coordinates]
        circle_elements = [self.generate_circle(c[0], c[1]) \
            for c in coordinates]
        return text_elements + circle_elements

    def generate_circle(self, x, y, r=0.66145):
        circle_style = 'fill:#000000;stroke:none;stroke-width:0.264583'
        el = Circle.new(center=(x, y), radius=r)
        el.style = circle_style
        return el


if __name__ == '__main__':
    NewElement().run()

```

Click the menu `Extensions -> Custom -> NewElement` to create elements on the 
current layer of a drawing. The drawing below shows the results. 


<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext7/newelement.png" alt="new elements"> 
</div>

The code logic is simple. The `add_line` method of the `NewElement` class shows four 
way to create a new `Line` element and set its attributes. The `set` method of an 
element such as `el1` seems to be the most reliable way to set attributes. 

The custom element classes do not have a custom `__init__` method. This is due to 
a requirement from `lxml` because they are inherited from `ElementBase`. 

## GenerateExtension Class

Many system extensions like `render_gears` and `render_barcode` inherit from `GenerateExtension` 
class. The class itself is a subclass of `EffectExtension`, and it already has code to add 
elements to the drawing. The source code is in the `inkex/extensions.py` module. When we 
inherit from this class, we only need to override the `generate` method. 

Here is an example of using `GenerateExtension` to create four lines. We do not need to 
write any code to deal with layers. The example below creates a new `lines` layer 
and adds new elements to the layer. 

```python
import inkex
from inkex import Line

class NewElement(inkex.GenerateExtension):
    container_label = 'lines'
    container_layer = True

    def generate(self):
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : '0.264583'}
        lines = self.add_lines()
        for l in lines:
            yield l

    def add_lines(self):
        el1 = Line()
        el1.set('x1', '10')
        el1.set('y1', '10')
        el1.set('x2', '40')
        el1.set('y2', '40')
        el1.set('style', self.style)

        el2 = Line.new(start=(40, 10), end=(10, 40))
        el2.style = self.style
        
        el3 = Line()
        el3.update(**{
            'x1': '50', 
            'y1': '10', 
            'x2': '80', 
            'y2': '40',
            'style': self.style
        })

        el4 = Line(x1='50', y1='40', x2='80', y2='10')
        el4.style = self.style

        return el1, el2, el3, el4


if __name__ == '__main__':
    NewElement().run()
```

## Inkex SVG Parsing 

When we load an XML file into memory, we usually use the default XML parser that comes with 
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
[using custom Element classes in lxml](https://lxml.de/element_classes.html). The 
"Tree based element class lookup in Python" section has an example like this. 

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

The code in the `elements/_base.py` module follows this model to define the lookup 
class `NodeBasedLookup`. It creates a custom parser `SVG_PARSER` and defines the `load_svg` 
method which uses the parser. 


With the parser in place, the return value from `etree.parse` method will contain `Rectangle` 
class object instead of general `Element` object if it is an `rect` shape element. 
This is a simplification. It actually is a Python proxy object because `lxml.etree` is 
based on libxml2, which loads the XML tree into memory in a C structure. 





