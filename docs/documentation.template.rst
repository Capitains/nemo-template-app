Documentation : Templates
=========================



Templates
~~~~~~~~~

The Template system behind Nemo is the `Jinja
template <http://jinja.pocoo.org/docs/2.10/>`__.

Templates are stored in the ``./templates`` folder for this application.
All mandatory templates are available in the
```./templates/main`` <./templates/main>`__ directory. **You should not
remove any of them in case you have forgotten an inclusion. You can
however not use them if you wish to.**

For any one wanting to completely dive in, we recommend reading `*The
Flask Mega Tutorial Part II :
Templates* <https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates>`__
by Miguel Grinberg.

However, the important syntax bits to understand are the following :

Showing a Variable
^^^^^^^^^^^^^^^^^^

``{{variable_name}}`` is used to show the value of a variable in the
code.

For example, ``<a class="{{class}}">{{page_name}}</a>`` will show
``<a class="css-class">Lorem Ipsum</a>`` if ``class`` and ``page_name``
variables have ``css-class`` and ``Lorem Ipsum`` values.

Doing a condition
^^^^^^^^^^^^^^^^^

Conditions are written wrapping some content between
``{% if condition %}`` and ``{% endif %}``. Conditions follow the python
syntax, here are some examples :

-  ``if a == b`` checks the equality between a and b variable
-  ``if a == "b"`` checks the equality between the variable a and the
   text ``b``
-  ``if "a" in some_list`` checks if the text ``a`` is in the list
   ``some_list``
-  ``if "a" not in some_list`` checks if the text ``a`` is not in the
   list ``some_list``
-  ``if a`` checks if the value behind ``a`` is truish (not an empty
   list, string or dictionary, or actually ``True``
-  ``if not a`` check if the variable ``a`` is empty or False

**Eg.**

.. code:: html

    {% if has_about_route or additional_pages %}
    <header>
        <span class="content">Project</span>
    </header>
    {% endif %}

will show the html if ``has_about_route`` variable or
``additional_pages`` variable are either true or not empty

Blocks and block extension
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you look in the templates, you'll most likely find something like the
following

.. code:: html

    {% extends "main::container.html" %}

    {%block article%}
    <article>
        <h1>About page to be completed on a project basis</h1>
    </article>
    {%endblock%}

Blocks in Jinja are bits of templates that can be replaced by other
templates. Here, this templates open the
```./templates/main/container.html`` <./templates/main/container.html>`__
template and replace the content of the block named ``article`` with the
``<article>[...]</article>`` html.

Quite practical when we want to not duplicate code !

Dynamic URLs
^^^^^^^^^^^^

Dynamic URLs, or URLs based on the current instance, are recommended.
These URLs are built automatically by Flask and it makes sure you are
not hardcoding to many things.

The syntax for such links is
``{{url_for("name_of_the_route", optional_parameter=parameter_value, optional_parameter=parameter_value)}}``
with as many ``optional_paramater`` as it makes sense for the given
link. You can use variable for ``parameter_value``, int or string. If
you use string, the syntax is
``{{url_for("route", number=5, string="some_string", variable=some_variable)}}``

Nemo base templates
^^^^^^^^^^^^^^^^^^^

The Nemo base templates have specific variables given to them, and some
variable are sent accross all templates. You can find more about the
variable `in the Nemo
documentation <http://flask-capitains-nemo.readthedocs.io/en/latest/Nemo.templates.html#nemo-default-templates>`__

+----------------------------------+-----------------------------------------+
| Template Name                    | Role                                    |
+==================================+=========================================+
| `main/container.html <templates/ | Global container that is used by every  |
| main/container.html>`__          | page to not repeat css, javascript,     |
|                                  | etc.                                    |
+----------------------------------+-----------------------------------------+
| `main/footer.html <templates/mai | Container included in                   |
| n/footer.html>`__                | main/container.html for the footer      |
+----------------------------------+-----------------------------------------+
| `main/metadata.html <templates/m | Templates for metadata valid for every  |
| ain/metadata.html>`__            | pages (inserted in ``<head>``)          |
+----------------------------------+-----------------------------------------+
| `main/menu.html <templates/main/ | Template for menu shown on every page   |
| menu.html>`__                    |                                         |
+----------------------------------+-----------------------------------------+
| `main/404.html <templates/main/4 | Page displayed upon 404 errors          |
| 04.html>`__                      |                                         |
+----------------------------------+-----------------------------------------+
| `main/about.html <templates/main | Template displayed for the About Page   |
| /about.html>`__                  |                                         |
+----------------------------------+-----------------------------------------+
| `main/breadcrumb.html <templates | Template displayed for the breadcrumb   |
| /main/breadcrumb.html>`__        | in every page                           |
+----------------------------------+-----------------------------------------+
| `main/collection.html <templates | Template displayed for a browsing a     |
| /main/collection.html>`__        | collection                              |
+----------------------------------+-----------------------------------------+
| `main/index.html <templates/main | Template displayed at the index page    |
| /index.html>`__                  |                                         |
+----------------------------------+-----------------------------------------+
| `main/logo.html <templates/main/ | Template containing the upper left logo |
| logo.html>`__                    |                                         |
+----------------------------------+-----------------------------------------+
| `main/references.html <templates | Template used to display the list of    |
| /main/references.html>`__        | passages available for a text           |
+----------------------------------+-----------------------------------------+
| `main/text.html <templates/main/ | Template used to display a passage      |
| text.html>`__                    |                                         |
+----------------------------------+-----------------------------------------+
| `main/passage\_footer.html <temp | Template shown below a passage when     |
| lates/main/passage_footer.html>` | reading one.                            |
| __                               |                                         |
+----------------------------------+-----------------------------------------+
| `main/macros.html <templates/mai | Macros used accross templates. We       |
| n/macros.html>`__                | recommend not changing it               |
+----------------------------------+-----------------------------------------+

Linking to other pages
~~~~~~~~~~~~~~~~~~~~~~

You will find links here and there in the templates but here are the
main pages with their parameters. These routes are called using the
`{{url\_for()}} syntax <#dynamic-urls>`__.

-  ``r_index`` has no parameters. It's the index of the website
-  ``r_collections`` has no parameter. It leads to the main collection
   page.
-  ``r_collection`` takes an ``objectId`` parameter and optionally a
   ``semantic`` one to make a nice link. ``objectId`` represents the
   identifier of the collection to show. It displays children and
   metadat about a specific collection
-  ``r_first_passage`` takes an ``objectId`` parameter. It will redirect
   to the first passage of the text identified by the variable
   ``objectId``
-  ``r_passage`` takes an ``objectId`` and a ``subreference`` parameter.
   It will show the passage identified by ``subreference`` in the text
   identified by ``objectId``.
-  ``r_references`` takes an ``objectId`` parameter. It will show the
   list of available curated passages in the text identified by
   ``objectId``.
-  *(Optionally, depending on app configuration)* ``r_full_text`` takes
   an ``objectId`` parameter. It will full content of the text
   identified by ``objectId``.
-  *(Optionally, depending on app configuration)* ``r_about`` takes no
   parameter. It will show the about page
-  *(Optionally, depending on app configuration)* ``r_page`` takes a
   ``page_id`` parameter. It will show the page identified by the
   ``page_id`` parameter.

**Eg.**

.. code:: html

    <a href="{{url_for('.r_index')}}">Index</a>
    <a href="{{url_for('.r_collection', objectId='urn:cts:latinLit:phi1103.phi001')}}">Collection des Priapées</a>
    <a href="{{url_for('.r_first_passage', objectId='urn:cts:latinLit:phi1103.phi001.lascivaroma-lat1')}}">Premier passage des Priapées</a>
    <a href="{{url_for('.r_passage', objectId='urn:cts:latinLit:phi1103.phi001.lascivaroma-lat1', subreference='55')}}">Priapée 55</a>

will produce normally

.. code:: html

    <a href="/">Index</a>
    <a href="/collection/urn:cts:latinLit:phi1103.phi001">Collection des Priapées</a>
    <a href="/text/urn:cts:latinLit:phi1103.phi001.lascivaroma-lat1">Premier passage des Priapées</a>
    <a href="/text/urn:cts:latinLit:phi1103.phi001.lascivaroma-lat1/passage/55">Priapée 55</a>

Linking to Statics, JS and CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add or replace statics by adding file in the
```./statics/`` <./statics>`__ folder. These file can then be refered to
using the following syntax :
``{{url_for('.static', filename='path/from/statics')}}``.

**Eg**. the current ``/statics`` folder contains :

-  css

   -  bootstrap.min.css
   -  theme.min.css

-  images

   -  logo.png

If we want to refer to logo, we will type
``{{url_for('.static', filename='images/logo.png')}}``. And if we want
to insert it as an image, we will write

.. code:: html

    <img class="logo" src="{{url_for('.static', filename='images/logo.png')}} " alt="Capitains Nemo" />