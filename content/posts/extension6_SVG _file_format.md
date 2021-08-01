title: SVG File Format
slug: svg-file-format
date: 2021-07-31 15:50
category: extension
chapter: 6
note: SVG File Format

## SVG Format

The default Inkscape file is Scalable Vector Graphics (SVG) format. The SVG specification is 
an open standard developed by the World Wide Web (W3C) consortium. SVG files are XML text 
documents and all major modern web browers support SVG rendering.  

Let's create a new blank svg file and see what the code looks like. Launch the Inkscape and 
click the menu `File -> New` to create a new blank file, and save the file as 'new-drawing.svg'. 
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

The contents of the file is wrapped inside the `svg` tag ➋. The openning `svg` tag 
has many attributes. The attribute `xmlns:inkscape="www.inkscape..."` means that `inkscape` 
is an xml namespace.  So the attribute `inkscape:version="1.1..."` is an abbreviation for 
`www.inkscape...:version=....`. Inkscape is derived from another software `sodipodi`, and 
`sodipodi` is still a namespace. 

The `sodipodi:namedview` ➌ is an inkscape specific tag.  Inkscape will read and understand 
the tag and its attributes.  Other software does not have to recognize this tag. Notice 
it has an attribute named `current-layer` with value `layer1`. The current layer infomation 
is saved in the SVG file.  The `self.svg.namedview.center` value in `triangle.py` is 
also derived from this tag.  The `defs` should be an abbreviation for `definitions` ➍. 
We can store some information in the `defs` tag, and other 
tags can reference the `defs` tag.   

The `g` tag is a shorthand for group.  SVG itself does not have layer element. Inkscape uses 
group tag with additional attribute `groupmode` to represent layer ➎. 














