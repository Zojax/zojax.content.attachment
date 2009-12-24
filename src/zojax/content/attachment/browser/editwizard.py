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
import cgi
from zope import interface, component
from zope.location import LocationProxy
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.publisher.interfaces import NotFound
from zope.traversing.browser import absoluteURL
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.wizard.step import WizardStepForm
from zojax.content.browser.table import ContentsNameColumn
from zojax.content.type.interfaces import IContainerContentsTable
from zojax.content.attachment.interfaces import _, IAttachmentsExtension


class IWizardAttachmentsExtension(interface.Interface):
    pass


class AttachmentsStep(WizardStepForm):

    weight = 150
    title = label = _(u'Attachments')

    def update(self):
        self.attachments = LocationProxy(
            IAttachmentsExtension(self.getContent()), self.wizard, self.__name__)
        interface.alsoProvides(self.attachments, IWizardAttachmentsExtension)

        self.adding = getMultiAdapter((self.attachments, self.request), name='+')
        self.adding.update()

        super(AttachmentsStep, self).update()

    def publishTraverse(self, request, name):
        attachments = LocationProxy(
            IAttachmentsExtension(self.getContent()), self.wizard, self.__name__)
        interface.alsoProvides(attachments, IWizardAttachmentsExtension)

        if name in attachments:
            self.redirect('%s/'%absoluteURL(self, request))
            return self

        view = queryMultiAdapter((attachments, request), name=name)
        if view is not None:
            return view

        raise NotFound(self, name, request)


class ContentsNameColumn(ContentsNameColumn):
    component.adapts(IWizardAttachmentsExtension,
                     interface.Interface, IContainerContentsTable)

    def render(self):
        request = self.request
        content = self.content
        value = cgi.escape(self.query())

        if self.environ['url']:
            id = getUtility(IIntIds).queryId(content)

            return u'<a target="_blank" href="%s/@@content.attachment/%s/">%s</a>'%(
                absoluteURL(getSite(), request), id, value)
        else:
            return value
