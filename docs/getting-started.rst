.. _getting-started:

Getting started with supybot-github
===================================

Supybot-github should contain a few sane defaults to get you started.

.. _installation:

Installation
------------

0. `Install Limnoria`_ or any other supybot variant, and configure it to your
   liking.

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

.. _`Install Limnoria`: https://docs.limnoria.net/use/install.html

Development
-----------

In order to work on supybot-github, you normally have to set up an IRC server,
the supybot bot, and the rest of the configuration, as shown in
:ref:`installation`.

However, we are providing a command-line script to make your life a bit easier,
which returns the executed message without the rest of the hassle. Just follow
these instructions:

1. `Install Limnoria`_ or any other supybot variant. No further configuration
   is needed!

2. Run python in the plugin's directory, passing it a `.json` with Github's
   payload::

       python . samples/push-v3.json

After running the above, you should see a coloured output with the produced
message.
