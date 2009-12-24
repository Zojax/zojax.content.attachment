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
""" attachment implementation

$Id$
"""
from zope import interface, component
from zope.proxy import removeAllProxies
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from zojax.content.type.item import PersistentItem
from zojax.filefield.field import FileFieldProperty

from interfaces import IImage
from preview import PreviewFolder


class Image(PersistentItem):
    interface.implements(IImage)

    data = FileFieldProperty(IImage['data'])

    def __init__(self, **kw):
        super(Image, self).__init__(**kw)

        self.preview = PreviewFolder()
        self.preview.__parent__ = self

    def __nonzero__(self):
        return self.data.size > 0

    @property
    def width(self):
        return getattr(self.data, 'width', -1)

    @property
    def height(self):
        return getattr(self.data, 'height', -1)


@component.adapter(IImage, IObjectModifiedEvent)
def imageModifiedHandler(image, event):
    removeAllProxies(image).preview.clear()
