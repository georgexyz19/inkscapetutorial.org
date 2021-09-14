title: Transforms
slug: transforms
date: 2021-08-09 11:47
category: extension
chapter: 11
note: Transforms

## Equations

When we move an element from one location to another location on Inkscape canvas, we can 
also view it as moving an imaginary coordinate system with it. The element stays at the 
same location in the imaginary coordinate system. Translate, rotate, and scale are three 
common transforms in Inkscape. 

<div style="max-width:800px" class="text-center">
  <img class="img-fluid pb-2" src="/images/ext11/coordinate.svg" alt="coordinate-system"> 
</div>

The translate transform is simply moving an object.  The coordinate of a point on 
the object (x, y) will change to (x', y'). The `a` and `b` values in the equations 
shown below represent the distances along X and Y axles the object has moved. If 
we write two equations below in a matrix form, we have the third 
equation. 


<div style="max-width:800px" class="text-center">
  <img class="img-fluid pb-2" src="/images/ext11/equations.svg" alt="equation 1"> 
</div>

The two equations below are for rotation and scale. The rotation angle (alpha) is 
clockwise because the y axle increases from top to bottom. The `a` and `b` of 
the scale equation represent the scale factor along X and Y. 

<div style="max-width:800px;" class="text-center">
  <img class="img-fluid pb-2" src="/images/ext11/equations2.svg" alt="equation 2"> 
</div>

The above rotation equation is for rotating around origin (0, 0).  If we rotate an element 
around a coordinate (a, b), the equation becomes like this.

<div style="max-width:800px;" class="text-center">
  <img class="img-fluid pb-2" src="/images/ext11/equations2a.svg" alt="equation 2a"> 
</div>

The matrix is in this form when those three transforms are combined. 

<div style="max-width:800px" class="text-center">
  <img class="img-fluid pb-2" src="/images/ext11/equations3.svg" alt="equation 3"> 
</div>

## Inkscape Transforms

Let's look at an example to see how the transform works in Inkscape. First we draw 
a rectangle with top left coordinates (10, 10).  It has a width of 60 and height of 40. 
The SVG file has these lines for the element. We can ignore the `id` and `style` attributes 
for this example. 

```xml
<rect
    style="fill:none;stroke:#000000;
        stroke-width:0.26458333;stop-color:#000000"
    id="rect31"
    width="60"
    height="40"
    x="10"
    y="10" />
```

We will use the transform dialog (Menu `Object -> Transform` or shortcut Ctrl + Shift + M) 
to see how Inkscape handles transform. When we move the rectangle 10mm horizontally and 10mm 
vertically (with Relative move selected), the SVG element coordinates will change. 

```xml
<rect
    width="60"
    height="40"
    x="20"
    y="20" />
```

Next let's rotate the object 30 degrees clockwise. The element code becomes like this. 
It will has a new `transform` attribute with `rotate(30)` as its value. The x and y 
coordinate values change from (20, 20) to (33.3012, -10.3589). The reason is that 
the rotation is not around the origin (0, 0), instead it is around the center of the 
rectangle which is (50, 40). How does the Inkscape calculate the new coordinates 
of the top left corner of rectangle? It is a little complicated, and this 
[numpy python script](/files/coordinate_calc.py.txt) shows the calculation. 

```xml
<rect
    width="60"
    height="40"
    x="33.30127"
    y="-10.358984"
    transform="rotate(30)" />
```

The rotate function as the value of the `transform` attribute can also accept two additional 
arguments as the rotation center. The xml code shown below represents the same rectangle. 

```xml
<rect
    width="60"
    height="40"
    x="20"
    y="20"
    transform="rotate(30, 50, 30)" />
```

The SVG specs defines other transform functions `translate`, `scale`, `skewX`, `skewY`, and `matrix`. 
We can also add a transform attribute to a group or a layer. 

## Transform in Extension Code

The `transform.py` module in the `inkex` directory has over 1,000 lines of code. But the 
system extensions do not use this function very often.  Only a few system extensions 
set the `transform` attribute. 

Here is an simple extension to test `transform` attribute of rectangle element. 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<inkscape-extension 
    xmlns="http://www.inkscape.org/namespace/inkscape/extension">
    <name>Transform Element</name>
    <id>user.transform</id>
    <effect>
        <object-type>all</object-type>
        <effects-menu>
            <submenu name="Custom"/>
        </effects-menu>
    </effect>
    <script>
        <command location="inx" interpreter="python">transform.py</command>
    </script>
</inkscape-extension>
```

```python
# transform.py
import inkex
from inkex import Rectangle, Transform 

class NewElement(inkex.GenerateExtension):
    container_label = 'transform'
    container_layer = True

    def generate(self):
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : self.svg.unittouu('1px')}
        rects = self.add_rect()
        for r in rects:
            yield r

    def add_rect(self):

        el1 = Rectangle(x='10', y='10', width='60', height='40')
        el1.style = self.style

        el2 = Rectangle.new(20, 20, 60, 40)
        el2.style = self.style 
        tr = Transform('rotate(30)')
        el2.transform = tr

        el3 = Rectangle.new(20, 20, 60, 40)
        el3.style = self.style 
        tr = Transform('rotate(30, 50, 40)')
        el3.transform = tr

        el4 = Rectangle.new(20, 20, 60, 40)
        el4.style = self.style 
        tr = Transform('translate(10, 10) rotate(45)')
        el4.transform = tr

        el5 = Rectangle.new(20, 20, 60, 40)
        el5.style = self.style 
        tr = Transform('scale(2.0) rotate(60)')
        el5.transform = tr

        el6 = Rectangle.new(20, 20, 60, 40)
        el6.style = self.style 
        tr = Transform('rotate(60)') * Transform('scale(2.0)')
        el6.transform = tr

        return el1, el2, el3, el4, el5, el6


if __name__ == '__main__':
    NewElement().run()
```

Notice in the above examples, we can combine multiple transforms as 
the string argument to the `Transform` constructor, or multiply multiple 
`Transform` objects. The SVG results are shown below. 

```xml
    <rect
       x="10"
       y="10"
       width="60"
       height="40"
       id="rect1007" />
    <rect
       x="20"
       y="20"
       width="60"
       height="40"
       transform="rotate(30)"
       id="rect1009" />
    <rect
       x="20"
       y="20"
       width="60"
       height="40"
       transform="matrix(0.866025 0.5 -0.5 0.866025 26.6987 -19.641)"
       id="rect1011" />
    <rect
       x="20"
       y="20"
       width="60"
       height="40"
       transform="matrix(0.707107 0.707107 -0.707107 0.707107 10 10)"
       id="rect1013" />
    <rect
       x="20"
       y="20"
       width="60"
       height="40"
       transform="matrix(1 1.73205 -1.73205 1 0 0)"
       id="rect1015" />
    <rect
       x="20"
       y="20"
       width="60"
       height="40"
       transform="matrix(1 1.73205 -1.73205 1 0 0)"
       id="rect1017" />

```

## Other Classes

The `transforms` module also includes several other classes and functions.  The 
notable classes are `Vector2d`, `BoundingBox`, and `DirectedLineSegment`. It also 
defines two functions `cubic_extrema` and `quadratic_extrema`.  Those classes
and functions are not necessarily related to `transforms`. 

The `Vector2d` and `DirectedLineSegment` classes are very useful when we are working 
on mathematical drawings. We can apply vector algebra to calculate coordinates 
of points, and draw them as lines or polygons on the canvas. 

## References

Anthony J. Pettofrezzo published two books *Vectors and Their Applications* and 
*Matrices And Transformations*. Both books are relevant to the transforms module discussed in this chapter. 

The book *Mathematical Illustrations, A Manual Of Geometry and Postscript* by 
Bill Casselman is an excellent reference for math drawings. Here is the 
[link](https://personal.math.ubc.ca/~cass/graphics/manual/) to the book webpage. The pdfs of the book chapters are available on the webpage. 

The book *Introduction To Computer Graphics* by James Foley and others has a Chapter 
Geometrical Transformations. The transform equations in this book are in the 
same format as on this page. 