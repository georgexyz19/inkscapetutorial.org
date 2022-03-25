title: Selection
slug: selection
date: 2021-08-28 00:18
category: extension
chapter: 15
note: Selection

## Selection

One piece of information which Inkscape sends to an extension is selected elements. 
The extension receives ids of selected elements as command line arguments 
from Inkscape. 

For example, we have a drawing with 4 selected elements as shown below. When we click 
the `apply` button on an extension user interface, the extension receives 4 "--id=..." 
values as shown in the `sys.argv` variable below. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext15/selection-fig.png" alt="selection"> 
</div>

```
sys argv: ['hello.py', '--id=rect1125', '--id=path1149', 
            '--id=path1253', '--id=path1358', 
            '--name=inkscape', '/tmp/ink_ext_XXXXXX.svgUBQJ80']
```

The id values are the id attributes of selected elements.  Because the id attribute is unique 
for each element, the extension knows which elements are selected. 

The `inkex` uses `argparse` Python standard library module to parse arguments. The 
code is in the `__init__` method of `SvgInputMixin` class (inkex/base.py module). 

```
self.arg_parser.add_argument(
    "--id", action="append", type=str, dest="ids", default=[],
    help="id attribute of object to manipulate")

self.arg_parser.add_argument(
    "--selected-nodes", action="append", type=str, 
    dest="selected_nodes", default=[],
    help="id:subpath:position of selected nodes, if any")
```

The selected ids will become a list which is accessed as `self.options.ids` in an
extension.

```
self.options : Namespace(input_file='/tmp/ink_ext_XXXXXX.svgUBQJ80', 
                output=None, name='inkscape', 
                ids=['rect1125', 'path1149', 
                  'path1253', 'path1358'], selected_nodes=[]) 
```

When `inkex` loads an SVG file, it will set an instance variable `selection` 
on the `SvgDocumentElement` class object. The `selection` variable is of type 
`ElementList` and its value is set in the `load` method of `SvgInputMixin` class. 

```
self.svg = document.getroot()
self.svg.selection.set(*self.options.ids)
```

## ElementList Class

The `ElementList` class is defined in the `inkex/elements/_selected.py` module. 
Even though it is called `ElementList`, it subclasses `OrderedDict` so it's a 
dictionary.  When we iterate through an instance variable, it iterates through 
the values of the dictionary and the class acts like a list. The values of 
the dictionary are the selected element objects. 

We would think that keys of the dictionary are the ids of selected elements and 
the values are the corresponding element objects.  However, the keys are actually 
`xml_path` of selected element. The `xml_path` is a property defined in the 
`BaseElement` class and it calls the `getpath` method of `ElementTree` class. 
The [lxml documentation](https://lxml.de/api/lxml.etree._ElementTree-class.html#getpath) 
describes that "[getpath method] returns a structural, absolute XPath expression to find the 
element".  

`ElementList` key is a string value. It's the value before the colon as shown below. 
The first part `/*` refers 
to the `svg` element.  The second part `/*[3]` refers to `g` layer element nested inside `svg`. 
The `g` element is listed after `sodipodi:namedview` and `defs` elements. 
The third part `/*[1]` refers to the rect element, which is the first 
one nested under `g` element. 

```
# ELementList dict format: xml_path to element
/*/*[3]/*[1] : rect
/*/*[3]/*[2] : ellipse
/*/*[3]/*[3] : path
/*/*[3]/*[4] : path
```

The `ElementList` class also defines an `ids` instance variable, which is a 
dictionary mapping `id` to `xml_path`. The class also has a method `id_dict` 
which returns a dictionary mapping `id` to `element`. Why does the class choose 
to use `xml_path` value as the dictionary key? It is probably for the `paint_order` 
method which returns a list of selected elements by z-order (bottom to top). 


One very useful method in the `ElementList` class is `filter`. We can 
filter out elements by type. The method return a new `ElementList` object 
containing only elements of certain type. The code below shows an 
example, and the return value `selected_elems` only contains path elements. 

```
from inkex import PathElement
select_elems = self.svg.selection.filter(PathElement)
```

The `bounding_box` method returns a `BoundingBox` object for selected elements. 
It's useful when we need to know the size of selected elements such as 
the `Dimensions` extension. 

Inkscape itself preserves the selection order when passing the ids to an extension. 
The first element in the `ElementList` is the first selected element in Inkscape. 
The extension system doesn't provide a way to transmit selected elements back to 
Inkscape, so we can't modify selections in an Inkscape extension.

## Selected Nodes

Similar to selected elements, Inkscape also passes selected nodes to extensions. 
In inkscape we use the node selection tool (shortcut: F2) to select nodes on a path. For example, 
the drawing below shows that the first two nodes are selected (blue square dots).  When 
we click the apply button on an extension interface, the extension receives several 
`--selected-nodes=...` arguments. 

<div style="max-width:800px">
  <img class="img-fluid pt-2 pb-4" src="/images/ext15/node-sel.png" alt="node selection"> 
</div>

The argument values are in a format shown below. The help message of `add_argument` 
indicates it is in `id:subpath:position` format. Notice the `subpath` and `position` 
values are both zero based here. 

['path3535:0:1', 'path3535:0:0']

Searching through the system extension directory, the `selected-nodes` values 
are not used in any extensions.  However, it might be useful when we need to 
deal with path nodes in extensions. 

