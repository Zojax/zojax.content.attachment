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
from zope import interface, component
from zope.proxy import removeAllProxies
from zope.app.container.btree import BTreeContainer
from zope.app.container.interfaces import IObjectRemovedEvent
from zope.annotation.interfaces import IAttributeAnnotatable
from zojax.extensions.interfaces import IExtensionDataFactory
from zojax.extensions.container import ContentContainerExtension

from interfaces import IAttachmentsAware, IAttachmentsExtension


class AttachmentsExtension(ContentContainerExtension):
    interface.implements(IAttachmentsExtension)

    @property
    def _SampleContainer__data(self):
        data = self.data
        if data.__parent__ is None:
            data.__parent__ = removeAllProxies(self.context)
        return data


class ExtensionData(BTreeContainer):
    interface.implements(IAttributeAnnotatable)


class ExtensionDataFactory(object):
    component.adapts(IAttachmentsExtension)
    interface.implements(IExtensionDataFactory)

    def __init__(self, ext):
        self.extension = ext

    def __call__(self):
        data = ExtensionData()
        data.__parent__ = removeAllProxies(self.extension.context)
        return data


@component.adapter(IAttachmentsAware, IObjectRemovedEvent)
def contentRemoved(object, event):
    extension = IAttachmentsExtension(object)

    for key in list(extension.keys()):
        del extension[key]
