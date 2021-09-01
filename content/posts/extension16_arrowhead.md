title: Arrowhead Extension
slug: arrowhead-extension
date: 2021-08-30 13:13
category: extension
chapter: 16
note: Arrowhead Extension

## Problem

The `Dimension` system extension discussed in Chapter 14 adds markers as 
arrowheads for dimension lines. The markers have a stroke width which 
causes the arrowheads to extrude beyond leading lines. When we zoom in to 
the arrow heads, they look like this figure. 

<div style="max-width:500px">
  <img class="img-fluid pb-2" src="/images/ext16/arrowheads.png" alt="arrowheads"> 
</div>

If we manually set the marker stroke width to zero, it will have another 
problem. The tip of the arrow head is on top of the dimension line, and 
the arrowhead doesn't look good as shown below. 

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext16/arrowhead2.png" alt="arrowhead2"> 
</div>

What is the right way to draw the arrowhead? We should offset the start point 
of the dimension line by a distance `d`, so the arrowhead itself will cover the 
dimension line. Marker 
elements are often difficult to manupilate in Inkscape, so we will draw 
a filled path as arrowhead.  

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext16/distance.png" alt="distance"> 
</div>

This sounds like something which an Inkscape extension can do. Let's create 
such an extension. 

## Arrowheads

A simple arrowhead can be determined by two variables angle (A) and 
length (L). The angle is between two side lines (red) and the length is from 
the tip to the back of arrowhead (blue).  The extension will support 
two shapes `sharp` and `normal` as shown below. 

<div style="max-width:400px">
  <img class="img-fluid pb-2" src="/images/ext16/variables.svg" alt="variables"> 
</div>

Sometimes we need an arrowhead at one end of a 
path and sometimes we need it at both ends. The extension will support 
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

The dialog shown below is the extension user interface. When we use the 
extension, we need to draw a line on the canvas, have the line selected, 
and click the `Custom -> Draw Arrowhead` menu, choose the values on the 
dialog and click apply.  The extension Python code will add an arrowhead 
to the drawing and modify the selected path. 

<div style="max-width:400px">
  <img class="img-fluid pb-2" src="/images/ext16/interface.png" alt="interface"> 
</div>

