title: Element Classes
slug: element-classes
date: 2021-08-24 10:54
category: extension
chapter: 9
note: Element Classes

All element classes like `Polyline` and `TextElement` are directly or indirectly derived from 
`BaseElement` class, which is define in the `inkex/elements/_base.py` module. The 
`BaseElement` class is subclassed from `etree.ElementBase` class.  The `etree.ElementBase` 
class is described as "public Element class" in its 
[documentation page](https://lxml.de/api/lxml.etree.ElementBase-class.html). 

The `BaseElement` defines an `__init_subclass__` magic method which will register all 
its subclasses and add them to a `lookup_table` defined in `NodeBasedLookup` class. When 
the XML parser starts parsing a document, it will use this `lookup_table` 
to find appropriate custom element class for each element. It probably can be implemented 
as a class decorator in Python, but every `BaseElement` subclasses need to be decorated 
with the decorator.  

```
class BaseElement(etree.ElementBase):
    """Provide automatic namespaces to all calls"""
    def __init_subclass__(cls):
        if cls.tag_name:
            NodeBasedLookup.register_class(cls)
```
Here is a class hierarchy diagram for some element classes. 

<div style="max-width:800px">
  <img class="img-fluid pb-2" src="/images/ext14/elemclasses.svg" alt="elem classes"> 
</div>