title: lxml Basics
slug: lxml-basics
date: 2021-08-03 09:42
category: extension
chapter: 8
note: LXML Basics

## What is lxml

The Inkscape `SVG` files are in xml format. When we write an Inkscape extension, 
we could write the code to parse the xml, modify the 
content, and send it back to Inkscape. Or we can use other well 
designed and tested code for xml parsing and handling. In most cases, 
reusing existing code is a good thing which saves time. The 
drawback is that we have to spend time to learn how to use existing code. 

The [lxml](https://lxml.de/) 
XML toolkit is a Python binding for the C libraries libxml2 and libxslt. It is 
similar to Python standard library module `xml.etree.ElementTree`, but it is faster and 
easier to program. 
The Inkscape extension developers long recognized the value of `lxml` python 
package. The package `inkex` wraps many functions of `lxml` so extension 
developers do not have to deal with `lxml` directly in most cases.  

It is usually enough for Inkscape developers to only work with `inkex` package. 
But sometimes we want to use functionality in `lxml` directly, or try to understand 
the code in `inkex` package, so it's better to know the basics of `lxml` package. 

# Module etree

Main features of `lxml` package are in the `etree` module. We will discuss several 
functions and classes in the etree module in this chapter. 

Note terms like function, method, or class constructor may not be accurate. 
They are all callable objects in Python. In this chapter, we simply call them functions or methods. 

* etree.parse
* etree.ElementTree
* etree.tostring
* etree.fromstring
* etree.Element
* etree.SubElement
* etree.XML
* etree.XMLID

The `etree.parse` function is the quick way to convert an XML file into an `ElementTree`
object. The function accepts an XML file name (or file object) and an optional parser, 
and returns an `ElementTree` instance. 

```python
etree.parse(source, parser=None, base_url=None)
```

Here is a Python interpreter session showing how to load an SVG file. 

```
george@Inspiron-5515:~$ /usr/bin/python3
Python 3.9.5 (default, May 11 2021, 08:20:37) 
[GCC 10.3.0] on linux
>>> from lxml import etree
>>> doc = etree.parse('/home/george/Desktop/drawing-4.svg')
>>> doc
<lxml.etree._ElementTree object at 0x7fcbed555ac0>

>>> doc.getroot()
<Element {http://www.w3.org/2000/svg}svg at 0x7fcbed555d80>
>>> doc.getroot().tag
'{http://www.w3.org/2000/svg}svg'
>>> etree.__version__
'4.6.3'
```

The `etree.ElementTree` is a wrapper class around the `_ElementTree` class 
(which is a C++/C internal class or structure). We can 
call `etree.ElementTree()` method to create an empty document. If we pass a file name 
(or file object), the return value is an `ElementTree` instance. If we use the 
`element` argument, the file argument will be ignored. It returns an `ElementTree` 
object based on the `Element` object. 

The `etree.tostring` function converts an `ElementTree` or `Element` object 
to a string containing the XML content. The `etree.fromstring` function 
creates an `Element` object from a string. 

```python
etree.ElementTree(element=None, file=None, parser=None)
etree.tostring(elem_or_tree, pretty_print=False, encoding=None)
etree.fromstring(text, parser=None, base_url=None)
```

Here is an example testing those three methods. 

```
>>> et = etree.ElementTree(file='/home/george/Desktop/drawing-5.svg')
>>> et
<lxml.etree._ElementTree object at 0x7fcbeadd23c0>
>>> etree.tostring(et)
b'<!-- Created with Inkscape (http://www.inkscape.org/) --><svg ...'
>>> etree.tostring(et).decode('utf8')
'<!-- Created with Inkscape (http://www.inkscape.org/) --><svg ...'
>>> ss = etree.tostring(et).decode('utf8')
>>> etree.fromstring(ss)
<Element {http://www.w3.org/2000/svg}svg at 0x7fcbea9561c0>
```

The `Element` constructor creates and returns an object implementing 
the Element interface. The `SubElement` method creates a new `Element` 
object, and adds it as the 
next child of its parent element. It also returns the newly created element. 


Many old Inkscape extensions use `SubElement` method to add new elements before 
version 1.0. The `SubElement` method has one more argument `parent` than 
the `Element` constructor. The namespace part of XML is a little annoying to type. 
Here are a few examples.  

```python
etree.Element(tag, attrib={}, nsmap=None, **extras)
etree.SubElement(parent, tag, attrib={}, nsmap=None, **extras)
```


```python
>>> from lxml import etree
>>> rect = etree.Element('rect', x='50', y='50', width='30', height='20')

>>> etree.tostring(rect)
b'<rect x="50" y="50" width="30" height="20"/>'

>>> layer = etree.Element('g', attrib={'inkscape:label':'Layer 1', 
        'inkscape:groupmode': 'layer'})
Traceback (most recent call last): ...
ValueError: Invalid attribute name 'inkscape:label'

>>> INKNS = 'http://www.inkscape.org/namespaces/inkscape'
>>> NSMAP = {'inkscape': INKNS}

>>> layer = etree.Element('g', attrib={'{%s}label' % INKNS :'Layer 1', 
        '{%s}groupmode' % INKNS: 'layer'}, nsmap = NSMAP)

>>> etree.tostring(layer)
b'<g xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
        inkscape:label="Layer 1" inkscape:groupmode="layer"/>'

>>> layer.append(rect)
>>> etree.tostring(layer)
b'<g xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
        inkscape:label="Layer 1" inkscape:groupmode="layer">
            <rect x="50" y="50" width="30" height="20"/></g>'

>>> etree.SubElement(layer, 'rect', 
        attrib={'x': '100', 'y': '100', 'width': '50', 'height': '40'})
<Element rect at 0x7ff619336740>
>>> etree.tostring(layer)
b'<g xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
    inkscape:label="Layer 1" inkscape:groupmode="layer">
        <rect x="50" y="50" width="30" height="20"/>
        <rect x="100" y="100" width="50" height="40"/></g>'
```

The `etree.XML` function parses an XML document or fragment from a string and 
returns the root Element node.  It is similar to 
the `fromstring` method. 

The `etree.XMLID` function parses the text and returns a tuple (root_node, id_dict). 
The `root_node` is the same value returned by the `etree.XML` function. The 
`id_dict` contains id-element pairs. The dictionary keys are the `id` attributes 
of all elements, and the values are the elements referenced by the `id` attributes. 
We could design an SVG file and assign an `id` for each element, load the file with 
`etree.XMLID` function, and access element via the `id` attribute. 

```python
etree.XML(text, parser=None, base_url=None)
etree.XMLID(text, parser=None, base_url=None)
```

## Element Class

The `Element` object represents a node in the XML tree. It defines many instance methods 
and properties. [This webpage](https://lxml.de/api/lxml.etree._Element-class.html) 
lists the `Element` class API.  

The notable `Element` class properties are `tag` and `attrib`. The `tag` is the 
element tag name and `attrib` is the element attribute dictionary. 

```python
>>> el = etree.fromstring('<rect x="50" y="50" width="30" height="20"/>')
>>> el
<Element rect at 0x7f4b489aab40>
>>> el.tag
'rect'
>>> el.attrib
{'x': '50', 'y': '50', 'width': '30', 'height': '20'}
```

The `Element` instance acts like a Python list, with nested elements acting as 
members of the list. We can loop through an `Element` object, and it also supports 
slice operation. 

```python
>>> ss = '''<g xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" 
...     inkscape:label="Layer 1" inkscape:groupmode="layer">
...         <rect x="50" y="50" width="30" height="20"/>
...         <rect x="100" y="100" width="50" height="40"/>
...    <g> 
...        <line x1="10" y1="10" x2="40" y2="40"/>
...        <rect x="10" y="10" width="30" height="20"/>  
...    </g>     
... </g>'''
>>> et = etree.fromstring(ss)
>>> et
<Element g at 0x7ff52fe4c180>
>>> et.tag
'g'
>>> for e in et:
...   print(e.tag)
... 
rect
rect
g
>>> et[0:2]
[<Element rect at 0x7ff532a4ab80>, <Element rect at 0x7ff52fe50140>]

```

The `get` and `set` methods retrieves and assigns an attribute value, respectively. 
The class also has `append` and `insert` methods like a list. 
The `remove` method deletes an element child, and `clear` method removes all 
its child elements and attributes. 

```python
>>> et.get('{http://www.inkscape.org/namespaces/inkscape}label')
'Layer 1'
>>> et.set('id', 'g123252')
>>> et.get('id')
'g123252'

>>> r = etree.fromstring('<rect x="0" y="0" width="1" height="1"/>')
>>> et.append(r)
>>> [e.tag for e in et]
['rect', 'rect', 'g', 'rect']

>>> cir = etree.fromstring('<circle cx="10" cy="10" r="10" />')
>>> et.insert(0, cir)
>>> [e.tag for e in et]
['circle', 'rect', 'rect', 'g', 'rect']

>>> et.remove(cir)
>>> [e.tag for e in et]
['rect', 'rect', 'g', 'rect']

>>> import copy
>>> et_copy = copy.deepcopy(et)
>>> et_copy.clear()
>>> [e.tag for e in et_copy]
[]
>>> et_copy.tag
'g'
>>> et_copy.attrib
{}
```

The `getchildren` method returns a list of element children.  The `getiterator` 
method walks a subtree and looks for all descendants, and it also accepts a 
`tag` argument to look for a specific type of elements. The `getroottree` method 
return an `ElementTree` object which contains `Element` instance. It also has a 
`getparent` method which returns the parent element. 

```python
>> del et[-1]
>>> [e.tag for e in et ]
['circle', 'rect', 'rect', 'g']
>>> [e.tag for e in et.getchildren() ]
['circle', 'rect', 'rect', 'g']
>>> [e.tag for e in et.getiterator() ]
['g', 'circle', 'rect', 'rect', 'g', 'line', 'rect']
>>> [e.tag for e in et.getiterator(tag='rect') ]
['rect', 'rect', 'rect']

>>> tree = e.getroottree()
>>> tree
<lxml.etree._ElementTree object at 0x7ff52f59c740>

>>> et[-1]
<Element g at 0x7ff52f59a4c0>
>>> et[-1].getparent()
<Element g at 0x7ff52fe4c180>

```

The `find` method searches for element children and returns a single element 
that matches the pattern of its `path` argument. The `path` argument is 
a string describing the element for which we are searching. The values are 
in a format like `rect` or `g/rect`.  The `findall` method is similar to `find`, and 
it returns a list of child elements that match the pattern. But it does not 
search nested elements inside children. 

```python
>>> r1 = et.find('rect')
>>> r1.attrib
{'x': '50', 'y': '50', 'width': '30', 'height': '20'}

>>> r2 = et.find('g/rect')
>>> r2.attrib
{'x': '10', 'y': '10', 'width': '30', 'height': '20'}

>>> r3 = et.findall('rect')
>>> r3
[<Element rect at 0x7ff52f59ca80>, <Element rect at 0x7ff52f59cbc0>]
```

The `xpath` is the most complicated method in `Element` class, and it supports 
XPath search language. The XPath expressions support tests, operators, and functions. 
It works like `findall` in its simple form. Here are some of its common operators. 


* `/` searches for child element starting from itself
* `//` searches for itself and its descendant. 
* `e1|e2` combines the elements that matches e1 and e2. 
* `@attribute` returns attribute values 
* `e1[@attr=value]` elements with attribute value
* `*` wildcard matches all element or all attributes

```python
>>> et.xpath('rect')
[<Element rect at 0x7ff52f59ca80>, <Element rect at 0x7ff52f59cbc0>]

>>> et.xpath('/g')
[<Element g at 0x7ff52fe4c180>]
>>> et.xpath('/g/rect')
[<Element rect at 0x7ff52f59ca80>, <Element rect at 0x7ff52f59cbc0>]

>>> x1 = et.xpath('//rect')
>>> [x.tag for x in x1]
['rect', 'rect', 'rect']

>>> x2 = et.xpath('//rect|//g')
>>> [x.tag for x in x2]
['g', 'rect', 'rect', 'g', 'rect']

>>> x3 = et.xpath('//@width')
>>> x3
['30', '50', '30']
>>> et.xpath('//rect[@width=50]')
[<Element rect at 0x7ff52f59cbc0>]

>>> et.xpath('//@x')
['50', '100', '10']
>>> et.xpath('//rect[@x>10]')
[<Element rect at 0x7ff52f59ca80>, <Element rect at 0x7ff52f59cbc0>]

>>> et.xpath('/g/rect[position()=1]')  # position is a function
[<Element rect at 0x7ff52f59ca80>]

>>> x4 = et.xpath('//*')
>>> [x.tag for x in x4]
['g', 'circle', 'rect', 'rect', 'g', 'line', 'rect']

>>> et.xpath('//line/@*')
['10', '10', '40', '40']
```

Below is a function `find_or_create_layer` that calls the `xpath` method. 
The function searches existing layer names and returns the layer if it 
finds one, otherwise it creates a new layer and returns it. The function 
also shows how to deal with XML namespaces when we are working with `lxml`.  

```python
def find_or_create_layer(svg, name):
    # find an existing layer or create a new layer
    # need import inkex at the beginning of the module
    layer_name = 'Layer %s' % name
    path = '//svg:g[@inkscape:label="%s"]' % layer_name
    elements = svg.xpath(path, namespaces=inkex.NSS)
    if elements:
        layer = elements[0]
    else:
        layer = inkex.etree.SubElement(svg, 'g')
        layer.set(inkex.addNS('label', 'inkscape'), layer_name)
        layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
    return layer
```

## ElementTree Class

Most `ElementTree` class methods have the same function as in `Element` class. 
The notable methods are `getroot` and `write`.  The `getroot` method returns 
the root element, and it's the opposite of `getroottree` method of `Element` class. 
The `write` method serializes the `ElementTree` object back to XML file. 

```python
>>> r = tree.getroot()
>>> r
<Element g at 0x7ff52fe4c180>
>>> tree.write('/home/george/Desktop/temp.svg')
```

## References
 
Module `lxml.etree` official reference 

<span class="ml-4"></span>[https://lxml.de/apidoc/lxml.etree.html](https://lxml.de/apidoc/lxml.etree.html)


Python Standard Library Module `ElementTree`

<span class="ml-4"></span>[https://docs.python.org/3.9/library/xml.etree.elementtree.html](https://docs.python.org/3.9/library/xml.etree.elementtree.html)






