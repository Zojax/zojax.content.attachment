##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import os.path
import unittest, doctest
from zope import interface
from zope.app.rotterdam import Rotterdam
from zope.app.component.hooks import setSite
from zope.app.rotterdam import Rotterdam
from zope.app.intid import IntIds
from zope.app.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.testing import functional
from zope import event

from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.filefield.testing import ZCMLLayer, FunctionalBlobDocFileSuite
from zojax.content.space.interfaces import ISpace
from zojax.layoutform.interfaces import ILayoutFormLayer
from zojax.activity.interfaces import IActivityAware
from zojax.content.type.interfaces import IItem
from zojax.content.type.item import PersistentItem
from zojax.catalog.catalog import Catalog, ICatalog
from zojax.personal.space.manager import PersonalSpaceManager, IPersonalSpaceManager

from content import Content


class IDefaultSkin(ILayoutFormLayer, Rotterdam):
    """ skin """


zojaxAttachLayer = ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxAttachLayer', allow_teardown=True)


def setUp(test):
    root = functional.getRootFolder()
    setSite(root)
    sm = root.getSiteManager()

    # IIntIds
    root['ids'] = IntIds()
    sm.registerUtility(root['ids'], IIntIds)
    root['ids'].register(root)

    # catalog
    root['catalog'] = Catalog()
    sm.registerUtility(root['catalog'], ICatalog)

    # personal space manager
    root['people'] = PersonalSpaceManager()
    sm.registerUtility(root['people'], IPersonalSpaceManager)

    # default content
    content = Content()
    event.notify(ObjectCreatedEvent(content))
    root['content'] = content



def test_suite():
    tests = FunctionalBlobDocFileSuite(
        "testbrowser.txt",
        setUp=setUp,
        optionflags=doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)
    tests.layer = zojaxAttachLayer

    return unittest.TestSuite((tests,))
