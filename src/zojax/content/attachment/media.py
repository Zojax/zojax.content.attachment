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
import os.path

from zope import interface, component
from zope.proxy import removeAllProxies
from zope.app.container.interfaces import IObjectAddedEvent

from zojax.content.type.item import PersistentItem
from zojax.filefield.field import FileFieldProperty
from interfaces import IMedia
from preview import MediaPreviewFolder


class Media(PersistentItem):
    interface.implements(IMedia)

    data = FileFieldProperty(IMedia['data'])


    mediaType = IMedia['mediaType'].default

    autoplay = IMedia['autoplay'].default

    def __init__(self, **kw):
        super(Media, self).__init__(**kw)

        self.preview = MediaPreviewFolder()
        self.preview.__parent__ = self

    def __nonzero__(self):
        return self.data.size > 0


@component.adapter(IMedia, IObjectAddedEvent)
def mediaAddedHandler(media, event):
    if media.mediaType is None or not media.mediaType:
        removeAllProxies(media).mediaType = os.path.splitext(media.data.filename)[1][1:]
