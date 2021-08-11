title: Units and Coordinate Systems
slug: units-and-coordinate-systems
date: 2021-08-07 23:18
category: extension
chapter: 9
note: Units and Coordinate Systems

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

When we create a `Line` element and add it to the drawing, we usualy do not need to specify 
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
  <img class="img-fluid pb-2" src="/images/ext9/viewport.svg" alt="viewport"> 
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
the `stroke-width` attribue? The stroke width of `1px` is the same as `1/3.7795 = 0.2646mm`. 
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

