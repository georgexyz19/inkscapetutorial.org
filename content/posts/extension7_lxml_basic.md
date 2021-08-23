title: lxml Basics
slug: lxml-basics
date: 2021-08-03 09:42
category: extension
chapter: 7
note: LXML Basics

## What is lxml

The Inkscape `SVG` files are in xml format. When we write an Inkscape extension, 
we could write the code to parse the xml, modify the 
content, and send it back to Inkscape all by ourselves. Or we can use other well 
designed and tested code for xml parsing and handling. Normally 
reusing other people's code saves programming time, however the 
drawback is that we have to spend the time to learn how to use exising libraries. 

The [lxml](https://lxml.de/) 
XML toolkit is a Pythonic binding for the C libraries libxml2 and libxslt. It is 
similar to Python standard library module `xml.etree.ElementTree`, but it is faster and 
easier to program. 
The Inkscape extension developers long recognized the value of `lxml` python 
package. The package `inkex` wraps many functions of `lxml` so extension 
developers do not have to deal with `lxml` directly.  

It is usually enough for Inkscape developers to only work with `inkex` package. 
But sometimes we want to use functionality in `lxml` directly, or try to understand 
the code in `inkex` package. It is good to know the basics of `lxml` package. 

# Module etree

The `etree` module includes main features of `lxml` package. We will discuss several 
functions and classes in the etree modulue as listed below. 

Note the terminologies like function, method, or class constructor may not be acurate. 
They are all callable object in Python, and we can call those like a function. 

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

Here is a Python intepreter session showing how to load an SVG file. 

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

The `etree.ElementTree` is a wrapper class around the `_ElementTree` class. We can 
call `etree.ElementTree()` to create an empty document. If we pass a file name 
(or file object), the return value is an `ElementTree` instance. If we use the 
`element` argument, the file argument will be ignored. It returns an `ElementTree` 
object based on an `Element` object. 

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
Many Inkscape extensions use `SubElement` method to add new elements before 
version 1.0. The `SubElement` method has one more argument `parent` than 
the `Element` constructor. The namespace part of XML is a little annoying to type. 
Here are a few examples.  

```python
etree.Element(tag, attrib={}, nsmap=None, **extras)
etree.SubElement(parent, tag, attrib={}, nsmap=None, **extras)
```


```
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
returns the root Element node.  The functionality of `etree.XML` is similar to 
the `fromstring` method. 

The `etree.XMLID` function parses the text and returns a tuple (root_node, id_dict). 
The `root_node` is the same value returned by the `etree.XML` function. The 
`id_dict` contains id-element pairs. The dictionary keys are the `id` attributes 
of all elements, and the values are the elements referenced by the `id` attributes. 
We could design an SVG file and assign an `id` for each element, load the file with 
`etree.XMLID` function call, and access element via the `id` attribute. 

```python
etree.XML(text, parser=None, base_url=None)
etree.XMLID(text, parser=None, base_url=None)
```

## References
 
Module `lxml.etree` official reference 

<span class="ml-4"></span>[https://lxml.de/apidoc/lxml.etree.html](https://lxml.de/apidoc/lxml.etree.html)


Python Standard Library Module `ElementTree`

<span class="ml-4"></span>[https://docs.python.org/3.9/library/xml.etree.elementtree.html](https://docs.python.org/3.9/library/xml.etree.elementtree.html)






