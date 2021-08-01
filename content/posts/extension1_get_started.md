title: Get Started With Inkscape Extension
slug: extension-get-started
date: 2021-07-26 12:51
category: extension
chapter: 1
note: first tutorial on Inkscape Extension

## What Is Inkscape Extension?

Before we start developing Inkscape extensions (or plugins), let's look at one simple 
built-in extension and understand what is an Inkscape extension. 

After we lauch Inkscape, clik menu `Extensions -> Render -> Triangle...`. A new window 
will pop up on screen and it looks like this.  

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext1/ext1-triangle.png" alt="Triangle Ext Window"> 
</div>

If we click the `apply` button, the extension will draw a triangle on the Inkscape canvas. 
The three sides of the triangle are all of 100 px length.  We can also toggle the `live preview` 
box on and off to show a preview of the triangle. Obviously when the `Mode` is set to 
`From Three Sides` on the dialog, the extension program ignores the three `Angle` values. 

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext1/ext1-triangle-drawing.svg" alt="Triangle drawing"> 
</div>

Let's change the `Side length a (px)` value to 50 and re-apply the extension.  The program 
will create a triangle like this. 

<div style="max-width:300px">
  <img class="img-fluid pb-2" src="/images/ext1/ext1-triangle-drawing-2.svg" alt="Triangle drawing 2"> 
</div>

Next let's try to enter an invalid number and see the result.  Change the `Side length a (px)` 
value to 250. Note the length of a trangle side can't be longer than the sum of other two sides. 
The program will generate this error message. 

<div style="max-width:400px">
  <img class="img-fluid pb-2" src="/images/ext1/ext1-error.png" alt="Triangle error"> 
</div>

## What Extensions Can Do?

** AAAAAAAAAAAAAABBBBBBBBBBBBBB **

## Extension Programs

Most Inkscape extensions are written in Python programming language. If you are not familar 
with Python, 
[the official python tutorial](https://docs.python.org/3/tutorial/) is a good start point. 

Let's find out where the extension programs are located.  Click the menu `Edit -> Preferences` 
in Inkscape and choose `System` on the left panel. We can find two extension directory 
settings. The value in `User extensions` field is shown below.

```
/home/george/.config/inkscape/extensions
```

And here is the value of `Inkscape extensions` field.  We also call this `system 
extensions` directory. 

```
/usr/share/inkscape/extensions
```

My computer runs Ubuntu 21.04 OS, and Inkscape 1.1 is installed through 
`apt` commands as suggested on 
[this webpage](https://www.omgubuntu.co.uk/2021/05/inkscape-1-1-released-new-features). If you are running 
Inkscape under other OS, the directories will be different. 

The `user extensions` refers to extensions created by you as an Inkscape user. The 
`inkscape extensons` or `system extensions` refers to the programs that come with 
the Inkscape installation. We could put our extensions in the `inkscape extensions` 
directory, and they will run just fine. But it is better to seperate them and not 
modify system extensions. 

We can add two alias to the `~/.bashrc` file and have easier access to those two 
directories. 

```
alias cdsysdir='cd /usr/share/inkscape/extensions'
alias cduserdir='cd ~/.config/inkscape/extensions'
```

## System Extensions

Let's take a look at the `system extensions` directory and see what is there. 
The Linux commands below show that the directory has a total of 554 files and 
226 Python files. The fourth command below indicates that the Python files have 
a total of 43,979 lines of code.  

```bash
cd /usr/share/inkscape/extensions
find . -type f | wc -l        # 554  
find . -name '*.py' | wc -l   # 226
find . -name '*.py' -exec wc -l '{}' +    #43,979
```

The system extensions have lots of code, and it is probably not possible for 
one person to read and understand all of them.  This extension tutorial series
will try to explain a small subset of those files.  

If you want to take part in developing or improving those system extensions, 
this gitlab source code repository is the place to check out.  

[https://gitlab.com/inkscape/extensions/](https://gitlab.com/inkscape/extensions/)

## Inkscape Version and Extension

Inkscape versions 0.91 and 0.92 already come with many extensions. But they are 
mostly written in Python 2. I started using Inkscape regularly with version 0.92 and 
wrote a few extensions in Python 2. 

Even though Python 3.4 was released back in 2014 and many people were writting 
in Python 3, Inkscape extensions were still in Python 2 for many years. The 
reason is that most system extensions were created by various people over time
and it requires some work to convert them to Python 3. Note Python 
3 is not compatible with Python 2. 

Finally with the Inkscape 1.0 release, the extensions are upgraded to Python 3. 
The Inscape 1.1 extensions require Python 3.6 and above. If you somehow get an 
old Inkscape extension which does not run in version 1.1, try to load it 
with Inkscape 0.92.5 and it may work well. 

## Objectives

This tutorial series will not cover everything in Inkscape extension development. 
The articles are developed from my notes.  It is not as formal 
as a typical book or software manual, but it is in a much better shape than 
my notes. I am trying to point the right direction for beginners. 




