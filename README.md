# Nemo Template App

[![Build Status](https://travis-ci.org/Capitains/nemo-template-app.svg?branch=master)](https://travis-ci.org/Capitains/nemo-template-app)
[![Coverage Status](https://coveralls.io/repos/github/Capitains/nemo-template-app/badge.svg?branch=master)](https://coveralls.io/github/Capitains/nemo-template-app?branch=master)
[![License: MPL 2.0](https://img.shields.io/badge/License-MPL%202.0-brightgreen.svg)](https://opensource.org/licenses/MPL-2.0)
[![Live Demo : Site 1](https://img.shields.io/badge/Demo-Site%201-green.svg)](http://nemo-template-app-demo-prod.herokuapp.com/)
[![Read the Docs](https://img.shields.io/readthedocs/pip.svg)](https://nemo-template-app.readthedocs.io)


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
(Linux and MacOS) : you'll need to install python3. There is a [French tutorial](docs/python3-fr.md) and
 [English tutorial](docs/python3-en.md).
See [CONTRIBUTING.md](CONTRIBUTING.md) for more advises on how to do the
installations specific to the current repository.

## Documentation

Full documentation can be found at [https://nemo-template-app.readthedocs.io](https://nemo-template-app.readthedocs.io)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

### License

The software hereby presented is given to you under the Mozilla Public License 2.0.