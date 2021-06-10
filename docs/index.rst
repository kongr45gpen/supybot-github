.. supybot-github documentation master file, created by
   sphinx-quickstart on Fri Mar 18 15:54:33 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to supybot-github's documentation!
==========================================

**supybot-github** is a plugin for the python-based IRC bot `Limnoria`_ (and any
`Supybot`_ forks). Its purpose is to announce commits and other important
notifications from a `Github`_ repository on an IRC channel, using
`Github's webhooks`_.

The plugin is built to be highly configurable and extendable.
It's still in the beta phase, although it is quite usable.

Features
--------

Do note that most of these features are only partially complete:

- Support for a bunch of different Github events
- Support for `Travis`_ build notifications
- Support for Github `webhook secrets`_
- Different message themes
- A bunch of configuration options
- Increases the count of errors in your logs

.. _Supybot: https://sourceforge.net/projects/supybot/
.. _Limnoria: https://github.com/ProgVal/Limnoria
.. _Github: https://github.com/
.. _`Github's webhooks`: https://help.github.com/articles/about-webhooks/
.. _`Travis`: https://travis-ci.org/
.. _`webhook secrets`: https://developer.github.com/webhooks/securing/

Installation
------------

See :ref:`getting-started`.

Resources
---------

- Issue Tracker: https://github.com/kongr45gpen/supybot-github/issues
- Source Code: https://github.com/kongr45gpen/supybot-github

Support
-------

If you are having issues, please open up an issue at the
`issue tracker <https://github.com/kongr45gpen/supybot-github/issues>`_.

You can also pay a visit to the :code:`##alezakos` channel on the Libera.Chat IRC network.

Further Reading
---------------

.. toctree::
   :maxdepth: 2

   getting-started
   configuration
