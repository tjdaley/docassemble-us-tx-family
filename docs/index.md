---
layout: docs
title: Overview of docassemble-us-tx-family
short_title: Documentation
order: 20
---

**docassemble-us-tx-family** is a [docassemble] module targeting
Family Law applications in Texas.

# <a name="classes"></a>Classes

**docassemble-us-tx-family** defines the following [classes] which extend
[docassemble] classes:

* Income - Information relating to non-employment income, e.g. interest or child support.
* IncomeList - A list of Incomes
* Job - Information relating to income from employment
* JobList - A list of Jobs
* MyPeriodicValue - A PeriodicValue which is assumed to be filled in.

# <a name="functions"></a>Functions

**docassemble-us-tx-family** defines the following [functions]:

* Counties - Returns a list of counties in Texas suitable for populating a dropdown.
* Courts - Given the name of a county, returns a list of district courts suitable for populating a dropdown.

# <a name="files"></a>Static Files

To improve performance, certain [functions] create [static files]. For example, the *counties()* function
will look for a file called ```us-tx-counties.json```. If the file does not exist or is old, the *counties()* function will retrieve a list of counties from an internet resource and cache the results in ```us-tx-counties.json```. For now, this file is refreshed never refreshed after it is created.

* us-tx-counties.json
* us-tx-courts.json

# <a name="variables"></a>Variables

**docassemble-us-tx-family** tries to use as much of the base structure of [docassemble] as possible. This module exposes [variables] by extends=ing existing classes and creating some new ones. The legal class hierarchy in [docassemble] is robust and suggests extensions fit into a certain structure. I have not fitted everything in to this structure in a perfect way (e.g. *obligor* is not a member of *case* but perhaps should be). This is a very new API and is subject to radical change.

# <a name="questions"></a>Questions

To make certain [objects] easier to work with in interviews, **docassemble-us-tx-family** provides question files, some with generic objects. These interview segments are meant to be included into larger interviews. For example, the *employment_questions.yml* file will populate the *obligor*, *joblist*, and *incomelist* objects but is meant to be included into a larger interview such as one that creates a child support trial exhibit.

# <a name="forms"></a>Forms

Other question files, which have more formal-looking names, are intended to be full interviews that result in the creation of a letter, pleading, discovery document, or trial exhibit. These [forms] are the interviews that end users will access to create documents.

# <a name="toc"></a>Sections of the documentation

<ul class="interiortoc">
{% for section in site.data.docs %}
<li>{{ section.title }}</li>
<ul>
{% include docs_section.html items=section.docs %}
</ul>
{% endfor %}
</ul>

[classes]: {{ site.baseurl }}/docs/classes.html
[functions]: {{ site.baseurl }}/docs/functions.html
[static files]: {{ site.baseurl }}/docs/static_files.html
[variables]: {{ site.baseurl }}/docs/variables.html
[objects]: {{ site.baseurl }}/docs/objectgs.html

[docassemble]: https://docassemble.org
