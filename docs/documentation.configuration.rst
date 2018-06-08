Documentation : Configuration files
===================================


Configuration Files
~~~~~~~~~~~~~~~~~~~

The application is run by two general configuration files. They should
not be renamed nor should they be deleted. Configuration files have been
built around XML because that's something that people verse in TEI will
be familiar with. We are not saying it's the best technical system, but
it is the easiest to understand compared to JSON or YAML for most
humanists.

On top of that, if you use a good xml editor, each file is defined by a
scheme available in the folder
`configuration-schemas <./configuration-schemas>`__. These schemas are
documented.

corpora.xml
^^^^^^^^^^^

The ``corpora.xml`` file is **meant to define the corpus** (or corpora)
that you want to host with your application. It contains informations
such as the directories containing the `Capitains
corpora <http://capitains.org/pages/guidelines.html>`__.

You can find some example of small Capitains corpora at `Lasciva
Roma/Additional
Texts <https://github.com/lascivaroma/additional-texts>`__, `Lasciva
Roma/Priapeia <https://github.com/lascivaroma/priapeia>`__, and `Chartes
TNAH/Olivar Asselin <https://github.com/Chartes-TNAH/olivar-asselin>`__
which is an example of non classical corpora.

Typically, the ``corpora.xml`` file is divided into three main nodes
which we'll present here but you can find a more documented schema
`here <configuration-schemas/corpora.rng>`__.

Setting up cache
''''''''''''''''

The cache folder node (``<cache-folder>``) is a tool to specify the
directory that you are gonna use to cache processed informations. This
allows to speed the application by an order of magnitude when the
corpora are large.

Adding corpora
''''''''''''''

The ``<corpora>`` nodes contains the list of directories containing the
texts you want to serve.

**Eg.** :

.. code:: xml

    <corpora>
        <corpus>example_corpora/priapees</corpus>
        <corpus>example_corpora/other</corpus>
    </corpora>

Two corpus are imported, from both ``example_corpora/priapees`` and
``example_corpora/other`` directories.

Creating editorial collections
''''''''''''''''''''''''''''''

The ``<collections>`` nodes contains editorial collection that can be
used to make better entry point for the readers. This can overcome the
lack of editorialization or the aggregation of multiple corpora.

Setting up texts so that they are registered in a specific collection
                                                                     

While most nodes can be straightforward with the documentation, the
``<filters>`` one can be somewhat complicated. Let's see an example :

.. code:: xml

    <collection>
        <name lang="fre">Sources Latines</name>
        <identifier>latin_collection</identifier>
        <filters>
            <folder>example_corpora/priapees</folder>
            <folder>example_corpora/other</folder>
        </filters>
    </collection>

Here, we have a collection, identified by the ``latin_collection``
identifier, named "Sources Latines" in French. Texts will be
automatically stored in this collection if they are in the folder
``example_corpora/priapees`` **or** in the folder
``example_corpora/other``.

app.xml
^^^^^^^

This file is the file responsible for all things related to the Nemo
frontend : this will set up some options, give you the ability to add
static pages or make it possible to have nice proposed passages for your
users.

Let's talk about the main nodes

Adding the ability to see full texts instead of only passages
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

If the ``<full-text-route>`` node contains ``true``, Nemo will propose
for texts the ability to see the complete text and not only the passages
in it.

Adding an about route
'''''''''''''''''''''

If the ``<about-route>`` node contains ``true``, the application will
add an ``About`` page based on the HTML in the
```templates/main/about.html`` template <templates/main/about.html>`__

Setting up how passage of texts are grouped together
''''''''''''''''''''''''''''''''''''''''''''''''''''

Remember `the principles behind Nemo and
Nautilus <#whats-the-bigget-principle-behind-nemo-and-nautilus->`__ ?
Well, the thing is, the applications, unlike human, have basically no
idea how to show the text once they have been parsed. Should I show the
text per group of 30 lines ? What about when there is no lines ?

The ``<chunking>`` node will allow you to make manually curated passages
set with the ``<hardcoded>`` nodes or make curated semi-automatic
"passage groupers" based on the identifier of texts
(``<identifier-regexp>``) or their citation sytems
(``<citation-system>``).

**Eg.**:

.. code:: xml

    <chunking>
        <identifier-regexp level="1" level-name="Priapée {passage}">^urn:cts:latinLit:phi1103\..*$</identifier-regexp>
        <citation-system level="2" level-name="Chapitre {passage}" group-by="5">book,chapter</citation-system>
        <hardcoded identifier="urn:cts:aperire:delver.init.opp-lat1">
            <ref start="2" end="3">Leçon 2 et 3</ref>
        </hardcoded>
    </chunking>

1. Text matching the identifier regular expression
   ``^urn:cts:latinLit:phi1103\..*$`` will have

   a. their text named ``Priapée {passage}`` where ``{passage}`` will be
      replaced by the identifier of the current passage;
   b. their texts grouped at the level *one* (here, for these text, that
      would be the poem level);

2. Text that have their citation system in the exact form of ``book``
   then ``chapter`` will have

   a. their text named ``Chapitre {passage}`` where ``{passage}`` will
      be replaced by the identifier of the current passage;
   b. their texts grouped at the level *two*, so at the chapter level,
      and they will be grouped by *five*;

3. Text identified by ``urn:cts:aperire:delver.init.opp-lat1`` will have

   a. Only one reference shown when browsing available passage, and it
      will be named ``Leçon 2 et 3``

Setting up texts to be shown only as full texts
'''''''''''''''''''''''''''''''''''''''''''''''

The node ``<full-text-only>`` is dependant on the ``<full-text-route>``
node to be set to ``true``. This setting will set up selected or all
texts to be only available as a full text in the reading interface (but
not in the API !). This specifically makes sense for texts such as short
poems, single letters, inscriptions, etc.

This node can contain an attribute ``all="true"`` that will make all
texts only available as full texts, or you can specify which text will
be shown this way using ``<id>`` nodes.

Setting up XSLT and transformation of the TEI
'''''''''''''''''''''''''''''''''''''''''''''

The ``<xslts>`` node will set-up the XSLTs that needs to be used on
specific texts or by default. The default xslt is specified by a
``<default>`` node and other are identified by an ``<xsl>`` node.

**Eg.**

.. code:: xml

    <xslts>
        <default>xsl/default.xsl</default>
        <xsl identifier="urn:cts:pompei:cil004-01700.01776.manfred-lat1">xsl/inscription.xsl</xsl>
        <xsl identifier="urn:cts:aperire:delver.init.opp-lat1">xsl/copy.xsl</xsl>
    </xslts>

-  The default XSL is xsl/default.xsl
-  If the text identifier is
   ``urn:cts:pompei:cil004-01700.01776.manfred-lat1``, the app will use
   ```xsl/inscription.xsl`` <xsl/inscription.xsl>`__
-  If the text identifier is
   ``urn:cts:pompei:cil004-01700.01776.manfred-lat1``, the app will use
   ```xsl/copy.xsl`` <xsl/copy.xsl>`__

Adding additional static pages
''''''''''''''''''''''''''''''

You can add additional pages in the node ``<additional-pages>``.
Templates for these page must be saved in the ``templates/additional``
directory.

**Eg.** :

.. code:: xml

    <additional-pages>
        <page id="credits" template="credits.html">
            <link-title>Credits</link-title>
        </page>
    </additional-pages>

-  A new page ``/page/credits`` will be created :

   -  it will be using the template in
      ```templates/additional/credits.html`` <templates/additional/credits.html>`__
   -  it will be using the title ``Credits`` in the Menu

