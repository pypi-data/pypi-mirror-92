# -*- coding: utf-8 -*-
from collective.clamav import tests
from collective.clamav.testing import EICAR
from collective.clamav.testing import AVMOCK_FUNCTIONAL_TESTING  # noqa
from io import BytesIO
from os.path import dirname
from os.path import join
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser

import unittest


def getFileData(filename):
    """ return a file object from the test data folder """
    filename = join(dirname(tests.__file__), 'data', filename)
    return open(filename, 'rb').read()


class TestIntegration(unittest.TestCase):

    layer = AVMOCK_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        # disable auto-CSRF
        from plone.protect import auto
        auto.CSRF_DISABLED = True

        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.browser = Browser(self.layer['app'])
        self.browser.addHeader(
            'Authorization', 'Basic {0}:{1}'.format(
                TEST_USER_NAME,
                TEST_USER_PASSWORD,
            ),
        )

    def tearDown(self):
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        from plone.protect import auto
        auto.CSRF_DISABLED = False

    def test_atvirusfile(self):
        # Test if a virus-infected file gets caught by the validator
        self.browser.open(
            self.portal.absolute_url() + '/virus-folder/++add++File')
        control = self.browser.getControl(name='form.widgets.file')
        with BytesIO(EICAR) as virus_file:
            control.add_file(virus_file, 'text/plain', 'virus.txt')
        self.browser.getControl('Save').click()
        self.assertFalse('Eicar-Test-Signature' not in self.browser.contents)

        # And let's see if a clean file passes...
        self.browser.open(
            self.portal.absolute_url() + '/virus-folder/++add++File')
        control = self.browser.getControl(name='form.widgets.file')
        with BytesIO(b'Not a virus') as clean_file:
            control.add_file(clean_file, 'text/plain', 'nonvirus.txt')
        self.browser.getControl('Save').click()
        self.assertTrue('Item created' in self.browser.contents)

    def test_atvirusimage(self):
        # Test if a virus-infected image gets caught by the validator
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.browser.open(
            self.portal.absolute_url() + '/virus-folder/++add++Image')
        control = self.browser.getControl(name='form.widgets.image')
        image_data = getFileData('image.png')
        with BytesIO(image_data + EICAR) as virus_image:
            control.add_file(virus_image, 'image/png', 'virus.png')
        self.browser.getControl('Save').click()

        self.assertFalse('Changes saved' in self.browser.contents)
        self.assertTrue('Eicar-Test-Signature' in self.browser.contents)

        # And let's see if a clean file passes...
        self.browser.open(
            self.portal.absolute_url() + '/virus-folder/++add++Image')
        control = self.browser.getControl(name='form.widgets.image')
        with BytesIO(image_data) as clean_image:
            control.add_file(clean_image, 'image/png', 'nonvirus.png')
        self.browser.getControl('Save').click()
        self.assertTrue('Item created' in self.browser.contents)
