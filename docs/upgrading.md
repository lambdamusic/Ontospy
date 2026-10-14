---
title: Upgrading to 2.0
nav_order: 6
has_children: true
---

# Upgrading to 2.0

Ontospy version 2 provides new SHACL support, as well as it changes some of its internal dependencies (primarily, it moves from Django to Jinja for the HTML documentation part).

For the majority of users this upgrade shouldn't cause any issues, but since various internals have changed this release may be backward-incompatible for users that have created custom extensions building upon Ontospy's documentation generation code.

-   Please have a look at the [Django to Jinja migration](pages/django-to-jinja.html) page for more information

For the changes in each release since then, see the [changelog](pages/changelog.html).
