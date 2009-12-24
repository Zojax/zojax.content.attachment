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
""" file implementation

$Id$
"""
from zope import interface, component
from zope.size import byteDisplay
from zope.size.interfaces import ISized
from zope.schema.fieldproperty import FieldProperty
from zojax.content.type.item import PersistentItem
from zojax.filefield.field import FileFieldProperty

from interfaces import IFile, IFileAttachment


class File(PersistentItem):
    interface.implements(IFile)

    data = FileFieldProperty(IFile['data'])
    disposition = FieldProperty(IFile['disposition'])

    def __nonzero__(self):
        return self.data.size > 0


class Sized(object):
    component.adapts(IFileAttachment)
    interface.implements(ISized)

    def __init__(self, context):
        self.context = context

    def sizeForSorting(self):
        return "byte", self.context.data.size

    def sizeForDisplay(self):
        return byteDisplay(self.context.data.size)
