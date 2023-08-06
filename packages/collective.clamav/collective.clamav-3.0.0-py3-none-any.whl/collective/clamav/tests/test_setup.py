# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.clamav.testing import COLLECTIVE_CLAMAV_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:  # Plone < 5.1
    HAS_INSTALLER = False
else:
    HAS_INSTALLER = True


class TestSetup(unittest.TestCase):
    """Test that collective.clamav is properly installed."""

    layer = COLLECTIVE_CLAMAV_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_product_installed(self):
        """Test if collective.clamav is installed."""
        if HAS_INSTALLER:
            qi = get_installer(self.portal)
            installed = qi.is_product_installed('collective.clamav')
        else:
            installer = api.portal.get_tool('portal_quickinstaller')
            installed = installer.isProductInstalled(
                'collective.clamav')
        self.assertTrue(installed)

    def test_browserlayer(self):
        """Test that ICollectiveClamavLayer is registered."""
        from collective.clamav.interfaces import (
            ICollectiveClamavLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveClamavLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CLAMAV_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if HAS_INSTALLER:
            qi = get_installer(self.portal)
            qi.uninstall_product('collective.clamav')
            self.installed = qi.is_product_installed('collective.clamav')
        else:
            installer = api.portal.get_tool('portal_quickinstaller')
            installer.uninstallProducts(['collective.clamav'])
            self.installed = installer.isProductInstalled('collective.clamav')

    def test_product_uninstalled(self):
        """Test if collective.clamav is cleanly uninstalled."""
        self.assertFalse(self.installed)

    def test_browserlayer_removed(self):
        """Test that ICollectiveClamavLayer is removed."""
        from collective.clamav.interfaces import ICollectiveClamavLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveClamavLayer, utils.registered_layers())
