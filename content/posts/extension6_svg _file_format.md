title: SVG File Format
slug: svg-file-format
date: 2021-07-31 15:50
category: extension
chapter: 6
note: SVG File Format

## SVG Format

The default Inkscape file is Scalable Vector Graphics (SVG) format. The SVG specification is 
an open standard developed by the World Wide Web (W3C) consortium. SVG files are XML text 
documents and all major modern web browsers support SVG rendering.  

Let's create a new blank svg file and see what the code looks like. Launch Inkscape and 
click menu `File -> New` to create a new blank file, and save the file as `new-drawing.svg`. 
Open the file with a text editor (such as gedit in Ubuntu). Below is the code in the SVG file. 

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>      ➊
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="210mm"
   height="297mm"
   viewBox="0 0 210 297"
   version="1.1"
   id="svg15798"
   inkscape:version="1.1 (1:1.1+202106032008+af4d65493e)"
   sodipodi:docname="new-drawing.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">   ➋
  <sodipodi:namedview
     id="namedview15800"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="0.64052329"
     inkscape:cx="396.55076"
     inkscape:cy="561.25984"
     inkscape:window-width="1551"
     inkscape:window-height="970"
     inkscape:window-x="26"
     inkscape:window-y="23"
     inkscape:window-maximized="0"
     inkscape:current-layer="layer1" />     ➌
  <defs
     id="defs15795" />                      ➍
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1" />                         ➎
</svg>

```

The first line and second line are Inkscape SVG boilerplate code. The first line 
inidcates this is an XML file.  The second line is an XML comment. 

The contents of the file is wrapped inside the `svg` tag ➋. The opening `svg` tag 
has many attributes. The attribute `xmlns:inkscape="http://www.inkscape..."` means that `inkscape` 
is an xml namespace.  So the attribute `inkscape:version="1.1..."` is an abbreviation for 
`http://www.inkscape...:version=....`. Inkscape is forked from another software `sodipodi`, and 
`sodipodi` is still a namespace. 

The `sodipodi:namedview` ➌ is an inkscape specific tag. Inkscape will read and interpret 
the tag and its attributes.  Other software does not have to recognize this tag. Notice 
it has an attribute named `current-layer` with value `layer1`. The current layer information 
is saved in the SVG file.  The `layer1` value refers to the id of a `g` tag. 
The `self.svg.namedview.center` value in `triangle.py` (discussed in 
previous chapters) is also derived from this tag.  The `defs` is an abbreviation 
for `definitions` ➍. We can store some information in a `defs` tag, and other 
tags of the same document can reference the `defs` tag.   

The `g` tag is a shorthand for group.  SVG itself does not have layer element. Inkscape uses 
group tag with additional attribute `groupmode` to represent layers ➎. 

## Shapes

There are [six basic element shapes](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Basic_Shapes) 
in SVG specs: line, rect, circle, ellipse, polyline, and polygon. When we are working 
on a drawing in Inkscape, we can create three types rect, circle, and ellipse directly. 
Inkscape uses paths for other types. The example drawing below is created in Inkscape, 
and the SVG code is shown below. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext6/shapes.svg" alt="shapes"> 
</div>

```xml
<g
   inkscape:label="Layer 1"
   inkscape:groupmode="layer"
   id="layer1">
   <rect
      id="rect31"
      width="40"
      height="30"
      x="10"
      y="10" />
   <ellipse
      id="path135"
      cx="80"
      cy="25"
      rx="20"
      ry="15" />
   <circle
      id="path1280"
      cx="123.56148"
      cy="25.414518"
      r="14.997319" />
   <path
      d="m 11.386056,53.443756 35.2468,23.203125"
      id="path568" />
   <path
      sodipodi:type="star"
      id="path1777"
      inkscape:flatsided="false"
      sodipodi:sides="8"
      sodipodi:cx="265.96295"
      sodipodi:cy="215.55252"
      sodipodi:r1="52.037506"
      sodipodi:r2="26.018753"
      sodipodi:arg1="0.78539816"
      sodipodi:arg2="1.1780972"
      inkscape:rounded="0"
      inkscape:randomized="0"
      d="m 302.75903,252.34859 -26.83913,-12.75788 
      -9.95695,27.99932 -9.95694,-27.99932 
      -26.83913,12.75788 12.75788, ... z"
      transform="matrix(0.26458333,0,0,0.26458333,
      -3.5417846,8.6272505)" />
   <path
      d="M 88.033107,69.531115 C 108.42781,53.650369 
      124.06814,55.364785 141.88598,71.15598"
      id="path2216"
      sodipodi:nodetypes="cc" />
</g>
```

The star shape is an Inkscape specific element. When we open the 
drawing in another program, the star shape may be treated as a path element. 

## Paths

Path element is more complicated than basic shapes. It has a `d` attribute 
which consists of commands and values. The command is a single letter followed by 
a value or a coordinate. The uppercase command indicates parameters are absolute 
values, and lowercase command indicates relative values. 
The Mozilla *SVG Tutorial* has [more information on paths](https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths). 
Here is a list of the commands.  

M/m
: Move to 

L/l
: Line to

H/h
: Horizontal line to

V/v
: Vertical line to

Q/q
: Quadratic curve to

T/t
: Smooth quadratic curve to

C/c
: Cubic curve to

S/s
: Smooth cubic curve to

A/a
: elliptical arc to

Z/z
: Close the path


Inkscape itself has lots of functions built around paths. Most 
of those functions are listed under the top level menu `Path`. For example, we can choose a 
rectangle element and click the first sub-menu `Object to Path`, and the SVG tag of the 
element change from `rect` to `path` with correct `d` attribute. 

## References

This chapter covers the minimum SVG knowledge we need to know as Inkscape extension developers. 
There are many online resources to learn more about SVG format.  The Inkscape 
itself is a good tool to learn SVG.  We can select an element and open the XML Editor 
to see the code or save the SVG file and open it in a text editor.   

The SVG is an open standard by W3C. The Inkscape SVG follows version 1.1. 
The 1.1 version spec is at this link 
[https://www.w3.org/TR/SVG11/](https://www.w3.org/TR/SVG11/). 
The 2.0 version is at this link 
[https://www.w3.org/TR/SVG2/](https://www.w3.org/TR/SVG2/).


*O'Reilly* has published a book *SVG Essentials (2nd ed)*. It is a decent reference book. 

