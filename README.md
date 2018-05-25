# Nemo Template App

[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)

## Introduction

You can do a lot without diving into Python with this application, it's actually it's first goal.
This application will provide you a **way to generate a website** for TEI/Epidoc texts with a CTS API
**without doing any python**. This "web app generator" is based on [Capitains Nemo](https://github.com/capitains/flask-capitains-nemo)
and [Capitains Nautilus](https://github.com/capitains/nautilus).

Be warned : this application only works with files following the [Capitains Guidelines](http://capitains.org/pages/guidelines.html) !

Of course, you can actually go deeper, touch the python, modify some stuff in Nemo or Nautilus. Nautilus is a full scale app, you
can change some things in it but it's mostly meant as an application that can work by itself. On the other end, Nemo is meant to be
a skeleton for developers who would like to build their own website ! Here, we made it a little more configurable so you would not need
to do python for most trivial tasks, but if you want more customization that what you'll see is already offered, you'll unfortunately have to
follow the documentation of Nemo, do python and learn maybe using the [Nemo Tutorial](https://github.com/capitains/tutorial-nemo).

The original intent of this repository is to answer to a lack of good introductory tools and has been built for a workshop in Lyon
given by Thibault Clérice, and as a general effort to make Capitains technically and timely affordable.

### What's the bigget principle behind Nemo and Nautilus ?

Nemo and Nautilus are built on the idea behind Capitains that texts are some kind of
[Ordered Hierarchy of Content Objects](http://cds.library.brown.edu/resources/stg/monographs/ohco.html),
to put it simply, your text should be citable by some logical units which makes up passage. They can be in a hierarchy
(with different levels) such as the traditional poem anthology structure : poem -> stanza -> line.

### Note about the repository

The current application is in a working state and can be run as a demo. This application can only be run on Unix machines
(Linux and MacOS) : you'll need to install python3. There is a [French tutorial](docs/python3-fr.md).
See [CONTRIBUTING.md](CONTRIBUTING.md) for more advises on how to do the
installations specific to the current repository.

## Documentation

### Configuration Files

The application is run by two general configuration files. They should not be renamed nor should they be deleted.
Configuration files have been built around XML because that's something that people verse in TEI will be familiar with.
We are not saying it's the best technical system, but it is the easiest to understand compared to JSON or YAML for most
humanists.

On top of that, if you use a good xml editor, each file is defined by a scheme available in the folder
[configuration-schemas](./configuration-schemas). These schemas are documented.

#### corpora.xml

The `corpora.xml` file is **meant to define the corpus** (or corpora) that you want to host with your application. It contains
informations such as the directories containing the [Capitains corpora](http://capitains.org/pages/guidelines.html).

You can find some example of small Capitains corpora at [Lasciva Roma/Additional Texts](https://github.com/lascivaroma/additional-texts),
 [Lasciva Roma/Priapeia](https://github.com/lascivaroma/priapeia), and [Chartes TNAH/Olivar Asselin](https://github.com/Chartes-TNAH/olivar-asselin)
 which is an example of non classical corpora.

Typically, the `corpora.xml` file is divided into three main nodes which we'll present here but you can find a more
documented schema [here](configuration-schemas/corpora.rng).

#### `<cache-folder>`

The cache folder is a tool to specify the directory that you are gonna use to cache processed informations. This allows to
speed the application by an order of magnitude when the corpora are large.

#### `<corpora>`

The `<corpora>` nodes contains the list of directories containing the texts you want to serve.

#### `<collections>`

The `<collections>` nodes contains editorial collection that can be used to make better entry point for the
readers. This can overcome the lack of editorialization or the aggregation of multiple corpora.

##### `<filters>`

While most nodes can be straightforward with the documentation, the filter one can be somewhat complicated.
Let's see an example :

```xml
<collection>
    <name lang="fre">Sources Latines</name>
    <identifier>latin_collection</identifier>
    <filters>
        <folder>example_corpora/priapees</folder>
        <folder>example_corpora/other</folder>
    </filters>
</collection>
```

Here, we have a collection, identified by the `latin_collection` identifier, named "Sources Latines" in French.
Texts will be automatically stored in this collection if they are in the folder `example_corpora/priapees` **or**
in the folder `example_corpora/other`.

#### app.xml

This file is the file responsible for all things related to the Nemo frontend : this will set up some options,
give you the ability to add static pages or make it possible to have nice proposed passages for your users.

Let's talk about the main nodes

##### `<full-text-route>`

If set to `true`, Nemo will propose for texts the ability to see the complete text and not only the passages in it.

##### `<about-route>`

If set to `true`, the application will add an `About` page based on the HTML in the [`about.html` template](templates/main/about.html)

##### `<chunking>`

Remember
    <chunking>
        <identifier-regexp level="1" level-name="Priapée {passage}">^urn:cts:latinLit:phi1103\..*$</identifier-regexp>
        <citation-system level="2" level-name="Chapitre {passage}" group-by="5">book,chapter</citation-system>
        <hardcoded identifier="urn:cts:aperire:delver.init.opp-lat1">
            <ref start="2" end="3">Leçon 2 et 3</ref>
            <ref id="4">Leçon 4</ref>
            <ref id="5">Leçon 5</ref>
            <ref id="6">Leçon 6</ref>
            <ref id="7">Leçon 7</ref>
            <ref id="8">Leçon 8</ref>
            <ref id="9">Leçon 9</ref>
        </hardcoded>
    </chunking>
    <full-text-only>
        <id>urn:cts:pompei:cil004-01700.01776.manfred-lat1</id>
    </full-text-only>
    <xslts>
        <default>xsl/default.xsl</default>
        <xsl identifier="urn:cts:pompei:cil004-01700.01776.manfred-lat1">xsl/inscription.xsl</xsl>
        <xsl identifier="urn:cts:aperire:delver.init.opp-lat1">xsl/copy.xsl</xsl>
    </xslts>
    <additional-pages>
        <page id="credits" template="credits.html">
            <link-title>Credits</link-title>
        </page>
    </additional-pages>
### Linking to Statics, JS and CSS

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

### License

The software hereby presented is given to you under the Mozilla Public License 2.0.