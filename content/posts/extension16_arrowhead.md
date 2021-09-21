title: Arrowhead Extension
slug: arrowhead-extension
date: 2021-08-30 13:13
category: extension
chapter: 16
note: Arrowhead Extension

## Problem

The `Dimensions` system extension discussed in Chapter 14 adds markers as 
arrowheads. [Marker element](https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker) 
is an SVG concept and it has a stroke width which 
causes the arrowhead to extend beyond leading line. When we zoom in to 
the arrowheads, they look like this. 

<div style="max-width:500px">
  <img class="img-fluid pb-2" src="/images/ext16/arrowheads.png" alt="arrowheads"> 
</div>

If we manually set the marker stroke width to zero, we would have another 
problem. The tip of the arrowhead is on the top of dimension line, and 
the arrowhead doesn't look good (shown below). 

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext16/arrowhead2.png" alt="arrowhead2"> 
</div>

What is the right way to draw an arrowhead? We should offset the start point 
of the dimension line by a distance `d`, so the arrowhead itself will cover the 
dimension line. Marker 
elements are often difficult to manipulate in Inkscape, so we will draw 
a filled path as arrowhead.  

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext16/distance.png" alt="distance"> 
</div>

This sounds like something that an Inkscape extension can do. Let's create the 
arrowhead extension. 

## Arrowheads

A simple arrowhead can be determined by two variables&mdash;angle (A) and 
length (L). The angle is between two side lines (red) and the length is from 
the tip to the back of arrowhead (blue).  The extension will support 
two shapes `sharp` and `normal` as shown below. 

<div style="max-width:400px">
  <img class="img-fluid pb-2" src="/images/ext16/variables.svg" alt="variables"> 
</div>

Sometimes we need an arrowhead at one end of a 
path and other times we need it at both ends. The extension will support 
adding arrowhead at the begin, at the end, or at both ends. When we draw a 
straight line in Inkscape with the `Bezier` tool, the `d` attribute could 
have values like the values shown below.  The begin point is the coordinate after the `M` 
(Move), and end point is the second coordinate or a calculated coordinate 
based on values after `H` (Horizontal) or `V` (Vertical). Note the begin 
point could be on the right or top of end point.  

```
M 104.51948,88.538059 143.37506,72.466987
M 173.74472,28.097683 H 204.0094
M 183.58612,45.030754 V 74.30451
```

The dialog box below shows the extension user interface. When we use the 
extension, we need to draw a line on the canvas, have the line selected, 
and click the `Custom -> Draw Arrowhead` menu, choose the values on the 
dialog and click apply.  The extension Python code will add an arrowhead 
to the drawing and modify the selected path. The `draw_arrowhead.inx` file 
contains the extension GUI code and `draw_arrowhead.py` is the extension 
Python file. 

<div style="max-width:400px">
  <img class="img-fluid pb-2" src="/images/ext16/interface.png" alt="interface"> 
</div>

## Optimum Arrowhead Angles

What are the optimum arrowhead angles? The experiment drawing below shows all 
arrowheads with angles between 15 and 50 degrees with a 2.5 degree increment. 
Arrowheads with angle 25 or 30 look
nice and most arrowheads on my drawings have either 25 or 30 degree angles. The 
Python file `arrowhead_angle.py` is used to generate this drawing.  

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext16/anglesharp.svg" alt="sharp angle"> 
</div>

## Modify Dimensions Extension

We can modify the dimensions extension and use the arrowheads discussed in this 
chapter.  The drawing below shows the same figure discussed in Chapter 14. When we 
zoom in to the arrowheads, the tip of the arrowhead aligns well with the 
leading lines.  The revised code is in the `custom_dimensions.py` file. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext16/dimensionsrev.svg" alt="revised dimension"> 
</div>

<div style="max-width:600px">
  <img class="img-fluid pb-2" src="/images/ext16/arrowheadsrev.png" alt="arrowhead revised"> 
</div>

## Others

The extension program includes code to handle a two segment path. When we are working 
on a drawing, we often need to add arrowhead to such path. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext16/twosegment.svg" alt="two segment path"> 
</div>

The current arrowhead program is still simple and straightforward. It could become 
complicated. The current program does not handle curves, and adding curve support 
will become challenging. The code makes changes to the path, and we could save the 
original path information in the arrowhead element and retrieve it when we need 
it later.  
