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
from zopyx.txng3.core.exceptions import ConversionError
from zopyx.txng3.core.content import IndexContentCollector

from interfaces import IAttachmentsExtension


def getAttachmentsContent(content):
    extension = IAttachmentsExtension(content, None)
    if extension is None:
        return u''

    values = []
    collector = IndexContentCollector()
    for item in extension:
        item = extension[item]
        try:
            collector.addBinary(
                item.__name__, item.data.data,
                item.data.mimeType, raiseException=False, encoding='utf-8')
        except AttributeError:
            continue
        except ConversionError:
            continue

    return (u'\n'.join([y['content'] for x in collector.getFields()
                        for y in collector.getFieldData(x)])).strip()
