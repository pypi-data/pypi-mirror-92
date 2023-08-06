.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=================
collective.clamav
=================

.. image:: https://github.com/collective/collective.clamav/workflows/collective.clamav%20CI/badge.svg
    :target: https://github.com/collective/collective.clamav/actions?query=workflow%3A%22collective.clamav+CI%22

.. image:: https://coveralls.io/repos/github/collective/collective.clamav/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.clamav?branch=master

A product providing clamav antivirus integration for Plone sites with AT and Dexterity content types.
It does that by defining a validator which could be used with any content
type that uses File, Image or Named field(s). The open-source `Clam Antivirus` is
supported which is available for all platforms.



Usage
-----

- To start, you need to have ``clamd`` running on some host accessible by your instances. ``collective.clamav`` supports either UNIX socket connections or remote connections.

- Install collective.clamav and setup the host & port or the path to the ``clamd`` socket in the control panel (default is a network connection to ``clamd`` listening on *localhost* at port 3310). By default *Files* and *Images* are going to be checked for viruses when added or updated.


Adding anti-virus protection to non-ATFile based content
--------------------------------------------------------

If you want to add anti-virus protection to your custom AT content types
add the *isVirusFree* validator to your FileField(s). For instance::

      FileField('file',
        validators = (('isNonEmptyFile', V_REQUIRED),
                      ('isVirusFree', V_REQUIRED),),
        widget = FileWidget(label=u'File'),
      )

If you create custom Dexterity content types add only the necessary import statement to the
module and all plone.namedfile fields were automatically scaned::

    from Products.validation import V_REQUIRED)

Installation
------------

Install collective.clamav by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.clamav


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.clamav/issues
- Source Code: https://github.com/collective/collective.clamav
- Documentation: in the docs folder


Credits
-------


Some code was shamelessly borrowed from `pyClamd` and collective.ATClamAV:

-  Clam Antivirus: http://www.clamav.net
-  github: https://github.com/ggozad/collective.ATClamAV
-  pyClamd: http://xael.org/norman/python/pyclamd
-  github: https://github.com/collective.ATClamAV
-  github: https://github.com/davisagli/collective.ATClamAV



Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
