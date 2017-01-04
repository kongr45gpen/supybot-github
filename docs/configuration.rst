.. _configuration:

Configuring supybot-github
==========================

.. TODO: Update 19->20 when we have enough configuration variables

Supybot-github contains more than nineteen configuration variables available
for you to play with, switchable globally, per channel, or per repository.

Changing the configuration
--------------------------

The configuration variables for the plugin are managed by Supybot's native
configuration plugin, which means there is nothing different compared to any
other Supybot option or plugin.

All configuration options naturally reside in the ``supybot.plugins.Github``
group (note that option names are case-insensitive).

You can easily manipulate config options using your bot's ``config`` command:

>>> config list plugins.github
#allowArbitraryMessages, #alwaysShowForcedPushes, #brackets, #hidePush, #hideURL, ...

>>> config plugins.github.theme
default

>>> config plugins.github.theme compact # To set the theme to `compact`
The operation succeeded.

You can also change most of the configuration values for each channel:

>>> config channel "#main" plugins.github.hidePush true
The operation succeeded.

Changing the configuration in the URL
`````````````````````````````````````

Supybot-github also allows specifying most configuration options in the web hook
URL, provided that the :ref:`disallowConfigOverride <disallowConfigOverride-option>`
option is set to `False`. For example, if your default webhook URL is
``http://example.com:8093/``, you can request that messages are sent in the
``##commits`` channel, and set the configuration options ``shortURL=False``
and ``theme=compact`` by switching to this URL::

  http://example.com:8093/++commits/shortURL=False/theme=compact

Note that you can use the ``+``, ``~``, ``&`` and ``^`` symbols instead of the
normal ``#`` IRC channel prefix, to ensure that URLs work properly.

Available configuration values
------------------------------
``channel``
  The one IRC channel where notification messages should be sent by default
  (can be changed in the hook URL, unless the `disallowChannelOverride` option
  is set to True)

  :Default value: ``#commits``
  :Type: String
  :Scope: `Global`

``port``
  The port which will be used by the HTTP server to receive event information
  from Github and other services

  :Default value: `8093`
  :Type: Integer
  :Scope: `Global`

``shortURL``
  Whether to use https://git.io/ to make URLs to github pages shorter

  :Default value: `True`
  :Type: Boolean

``hidePush``
  Whether to hide the `User pushed .. commits into ...` message shown when a
  push is received

  .. image:: _static/hidePush.png
     :scale: 75

  Force-pushes will still be shown regardless of this settings, if
  ``alwaysShowForcedPushes`` is set to True.

  :Default value: `False`
  :Type: Boolean

``theme``
  The name of the theme that will be used to style IRC messages.

  .. image:: _static/theme.png
     :scale: 50

  Only two themes are currently available, ``default`` and ``compact``, which
  is based on the default theme, with less verbose and more organised commit
  notifications.

  You can create your own themes, using the provided ``CompactTheme.py`` and
  ``DefaultTheme.py`` classes as examples. Themes are expected to be stored in
  the ``local/theme/`` directory.

  :Default value: `default` (who would expect)
  :Type: String

``showMergedCommits``
  Whether to show all the old merged commits when a branch is merged into
  another branch

  :Default value: `False`
  :Type: Boolean

``showSuccessfulBuildMessages``
  Whether to show build messages for non-failing builds on CI services, such
  as Travis and AppVeyor. Setting to ``never`` will not show any message when
  a build is successful, setting to ``always`` will show all success messages,
  and setting this to ``change`` will only notify about successful builds, when
  the previous build was broken (i.e. whenever the build is fixed).

  :Default value: `change`
  :Possible values: ``never``, ``change``, ``always``
  :Type: Enum

``brackets``
  A set of characters to use instead of parentheses to enclose URLs. This may
  be useful if your IRC client considers the default parentheses part of the
  URL, resulting in wrong paths and 404 errors.

  .. image:: _static/brackets.png
     :scale: 75

  The ``brackets`` option is a string whose left half is the left bracket that
  will be placed before the URL, and whose right half is the right URL bracket.
  The middle character, if there is one, is ignored. This convention has the
  limitation that the left and right parts of the URL must have the same length.
  To bypass that, you can use the capital letter `M` to separate the string into
  left and right.

  **Examples:**

  =============  =================================
  ``brackets``                  URL
  =============  =================================
  *space*        ``https://git.io/v2tq4``
  ``()``         ``(https://git.io/v2tq4)``
  ``[]``         ``[https://git.io/v2tq4]``
  ``[ ]``        ``[https://git.io/v2tq4]``
  ``[M]``        ``[https://git.io/v2tq4]``
  ``--> <--``    ``-->https://git.io/v2tq4<--``
  ``-->  <--``   ``--> https://git.io/v2tq4 <--``
  ``->  M``      ``-> https://git.io/v2tq4``
  =============  =================================

  *NOTE:* Don't forget to quote (`"`) your bracket string when setting the
  configuration value on Supybot!

  :Default value: ``( )``
  :Type: String

``showMilestone``
  Shows the name of the issue's milestone, when a notification is shown for
  any issue update (if the milestone is specified).

  .. image:: _static/showMilestone.png
     :scale: 75

  Milestone updates will still be shown if this is set to False.

  :Default value: `True`
  :Type: Boolean

``tagShowCommitMsg``
  When a notification about a new tag is shown, display the message of the
  commit the tag is pointing to.

  :Default value: `True`
  :Type: Boolean

``hideURL``
  Whether to hide URLs for all actions.

  Useful for private repositories

  :Default value: `False`
  :Type: Boolean

``preventIssueNameSpam``
  If true, when many messages about the same Github issue are sent at the same
  time (e.g. when multiple labels are added), the issue name and URL will only
  be sent once, to reduce clutter.

  .. image:: _static/preventIssueNameSpam.png
     :scale: 75

  :Default value: `True`
  :Type: Boolean

``showIssueEdits``
  Whether to send a message when an issue is edited.

  :Default value: `True`
  :Type: Boolean

``showPendingStatuses``
  Whether to show a message for a "pending" status update by Github (e.g. when
  a Travis build starts)

  :Default value: `False`
  :Type: Boolean

``alwaysShowForcedPushes``
  Whether to always show force-pushes, regardless of the value of the `hidePush`
  option.

  :Default value: `True`
  :Type: Boolean

``disallowChannelOverride``
  Whether to force all commits to end up in the channel specified by the
  `channel` configuration option, ignoring the channel specified in the HTTP
  hook URL

  :Default value: `False`
  :Type: Boolean
  :Scope: `Global`

.. _disallowConfigOverride-option:

``disallowConfigOverride``
  Whether to ignore any configuration options provided in the HTTP hook URL

  If the ``disallowChannelOverride`` option is set to True, URLs will still be
  able to specify the notification's IRC channel, regardless of this setting.

  :Default value: `True`
  :Type: Boolean
  :Scope: `Global`

``allowArbitraryMessages``
  Whether to allow raw messages and colours to be sent to channels using HTTP
  (this does not bypass other security options). Useful when you want to use a
  tool that reports results on IRC via your supybot.

  :Default value: `False`
  :Type: Boolean
  :Scope: `Channel`
