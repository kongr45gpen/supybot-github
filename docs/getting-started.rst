.. _getting-started:

Getting started with supybot-github
===================================

Supybot-github should contain a few sane defaults to get you started.

Installation
------------

1. Go to one of supybot's plugin folders and clone the plugin in a directory
   called `Github`::

       git clone https://github.com/kongr45gpen/supybot-github.git Github

   It's important to have the plugin stored in a directory called `Github`, so
   that supybot's :code:`@load Github` and :code:`@unload Github` commands work
   properly.

2. Ask supybot in IRC to load the plugin for you::

        /msg my_awesome_bot load Github

3. Set the channel where Github's notifications will be sent by default::

        /msg my_awesome_bot config plugins.github.channel ##alezakos

4. Create a webhook for your repository in Github's settings panel. Point it to
   port `8093` of supybot's host machine::

       http://www.example.com:8093/

This should be enough to get you started!
If everything was set up correctly, your bot should drop an inspiring quote on
the channel you configured in the 3rd step.
