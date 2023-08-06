.. -*- mode: rst -*-

|Travis| |Wheel| |GithubRepo| |GithubRelease| |PyPiPackage|

|License| |Maintenance| |PyPiStatus|

.. |Travis| image:: https://travis-ci.com/m1ghtfr3e/ANF-Feed.svg?branch=main
    :target: https://travis-ci.com/m1ghtfr3e/ANF-Feed
 
.. |License| image:: https://img.shields.io/github/license/m1ghtfr3e/ANF-Feed?style=plastic
    :alt: License
  
.. |Wheel| image:: https://img.shields.io/pypi/wheel/ANF-Feed?style=plastic   
    :alt: PyPI - Wheel
 
.. |GithubRepo| image:: https://img.shields.io/github/repo-size/m1ghtfr3e/ANF-Feed?style=plastic   
    :alt: GitHub repo size
   
.. |Maintenance| image:: https://img.shields.io/maintenance/yes/2021?style=plastic   
    :alt: Maintenance
    
.. |PyPiStatus| image:: https://img.shields.io/pypi/status/ANF-Feed?style=plastic  
    :alt: PyPI - Status
    
.. |GithubRelease| image:: https://img.shields.io/github/v/release/m1ghtfr3e/ANF-Feed?color=purple&include_prereleases&style=plastic   
    :alt: GitHub release (latest by date including pre-releases)
    
.. |PyPiPackage| image:: https://badge.fury.io/py/ANF-Feed.svg
    :target: https://badge.fury.io/py/ANF-Feed

========
ANF Feed 
========


This is an Application to read RSS Feeds
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

  $ pip install ANF-Feed

- Cloning this Repo

You can also install it with cloning this repository::

  $ git clone https://github.com/m1ghtfr3e/ANF-Feed.git
  
  or via Github CLI:
  
  $ gh repo clone m1ghtfr3e/ANF-Feed

  $ cd ANF-Feed
  $ pip install -r requirements.txt

Optionally you can pip install it locally::

  $ pip install .



Usage
-----
After installation you have two options to start:

- Calling the __main__ of the package::

  $ python3 -m anfrss
  
  or
  
  $ python -m anfrss

- Or using the entry point. In this case you can
  just enter::

  $ anfrss




Meta
----
:Authors:
  m1ghtfr3e
:Version:
  0.0.1.dev3
