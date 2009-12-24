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
from zope import component
from zope.app.container.interfaces import IObjectAddedEvent

from zojax.topcontributors.api import contribute
from zojax.ownership.interfaces import IOwnership

from interfaces import IAttachment


@component.adapter(IAttachment, IObjectAddedEvent)
def attachmentAddedHandler(attach, event):
    content = attach.__parent__.__parent__
    ownership = IOwnership(content, None)
    if ownership is not None:
        contribute(content, ownership.ownerId, 1)
