.. image:: https://travis-ci.com/m1ghtfr3e/ANF-Feed.svg?branch=main
    :target: https://travis-ci.com/m1ghtfr3e/ANF-Feed

.. image:: https://img.shields.io/github/license/m1ghtfr3e/ANF-Feed?style=plastic

===============
ANF Feed Reader
===============

This is an Application to get and read RSS Feeds
from `ANFNews <https://anfenglishmobile.com>`__

Currently following languages are supported:
  - English (default)
  - German
  - Kurmanjî
  - Spanish
  - Arab

  *Languages can be changed during usage in the Menu Bar
  (left upper corner of the window)*

Installation
------------

- Via PyPi

The easiest installation would be over PyPi, via ``pip``
which is unfortunately not available right now,
but very soon::

  $ pip install anffeed

- Alternative

You can also install it with cloning this repository::

  $ git clone https://github.com/m1ghtfr3e/ANF-Feed-Reader.git
  $ cd ANF-Feed-Reader
  $ pip install -r requirements.txt

Optionally you can pip install it locally::

  $ pip install .



Usage
-----
After installation you have two options to start:

- Calling the __main__ of the package::

  $ python3 -m anfrss

- Or using the entry point. In this case you can
  just enter::

  $ anfrss




Meta
----
:Authors:
  m1ghtfr3e
:Version:
  0.0.1.dev1
