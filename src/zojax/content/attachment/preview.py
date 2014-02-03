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
import os.path, logging
from zope import interface, event
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.container.btree import BTreeContainer

from zojax.filefield.data import File
from zojax.converter.api import convert
from zojax.converter.interfaces import ConverterException, ConverterNotFound

import browser

from interfaces import IPreviewFolder
logger = logging.getLogger('zojax.content.attachment')


class PreviewFolder(BTreeContainer):
    interface.implements(IPreviewFolder)

    __name__ = u'preview'

    def clear(self):
        for name in list(self.keys()):
            del self[name]

    def generatePreview(self, width, height, mt='image/jpeg', quality=88):
        name = '%sx%s'%(width, height)
        if name in self:
            return self[name]

        image = self.__parent__

        if not image:
            return

        try:
            data = convert(image.data.data, 'image/jpeg',
                           sourceMimetype = image.data.mimeType,
                           width=width, height=height, quality=quality)
        except ConverterException:
            logger.warning('Conversion Error:', exc_info=True)
            return

        preview = File()
        preview.data = data
        preview.filename = name
        preview.mimeType = u'image/jpeg'
        event.notify(ObjectCreatedEvent(preview))

        self[name] = preview
        return self[name]


class MediaPreviewFolder(BTreeContainer):
    interface.implements(IPreviewFolder)

    __name__ = u'preview'

    def clear(self):
        for name in list(self.keys()):
            del self[name]

    def generatePreview(self, width, height, mt='image/jpeg', quality=88):
        name = '%sx%s'%(width, height)
        if name in self:
            return self[name]

        media = self.__parent__

        if not media:
            return

        try:
            data = convert(open(os.path.join(
                        browser.__path__[0], 'media_icon.gif')).read(),
                           'image/jpeg', sourceMimetype = 'image/gif',
                           width=width, height=height, quality=quality)
        except (ConverterException,ConverterNotFound), e:
            logger.warning('Conversion Error:', exc_info=True)
            return

        preview = File()
        preview.data = data
        preview.filename = name
        preview.mimeType = u'image/jpeg'
        event.notify(ObjectCreatedEvent(preview))

        self[name] = preview
        return self[name]
