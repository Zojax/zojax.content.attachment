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
from zojax.table.interfaces import ITableConfiguration
from zojax.content.type.interfaces import IContainerContentsTable
from zojax.content.attachment.interfaces import IAttachmentsExtension


class TableConfiguration(object):
    interface.implements(ITableConfiguration)
    component.adapts(IAttachmentsExtension,
                     interface.Interface, IContainerContentsTable)

    pageSize = 0
    enabledColumns = ('id', 'icon', 'name', 'title', 'size', 'type')
    disabledColumns = ()

    def __init__(self, context, request, extension):
        pass
