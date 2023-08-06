# -*- coding: utf-8 -*-
"""Init and utils."""
from Products.validation import validation
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('collective.clamav')


from collective.clamav.validator import ClamavValidator  # noqa

validation.register(ClamavValidator('isVirusFree'))
