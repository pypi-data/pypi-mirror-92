Changelog
=========

3.0.0 (2021-01-25)
------------------

- Remove the AT schema extension and make it work within Plone 5.2
  and Python 3. [Andreas Mantke]
- Increase the release number to 3 because it breaks compatibility
  to old Archetypes content types. [Andreas Mantke]
- Added a test for value NOT_CHANGED to the validator module because
  of a change in converter.py of plone.formwidget.namedfile [Andreas Mantke]
- isort and flake8 fixes in validator module [Andreas Mantke]
- Fix tests for Plone 5.2, discontinue Travis and switch to Github Actions
  [tschorr]



2.0a2 (2016-09-12)
------------------

- Fix ReST/pypi page syntax.
  [timo]


2.0a1 (2016-09-12)
------------------

- Initial release based on collective.ATClamAV with a new controlpanel module
  and and a configuration configlet for Plone 5 compatibility. The product
  and release works with Dexterity content types. [andreasma]

- Complete Plone 5 compatibility and transferring and adapting tests from
  collective.ATClamAV.
  [sneridagh]
