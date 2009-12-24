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
from zope import component, interface
from zope.component import getUtility
from zope.proxy import removeAllProxies
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds
from zope.traversing.browser import absoluteURL, AbsoluteURL
from zojax.wizard.step import WizardStep
from zojax.content.forms.form import AddForm
from zojax.content.forms.interfaces import IContentViewStep
from zojax.content.type.interfaces import IContentViewView
from zojax.content.attachment.interfaces import IAttachment


class AddAttachmentForm(AddForm):

    def getName(self, object=None):
        name = self.request.get('add_input_name', '')
        if not name and object is not None:
            name = object.data.filename

        return name

    def nextURL(self):
        container = self.context.__parent__.__parent__
        return '%s/%s/context.html'%(
            absoluteURL(container, self.request), self._addedObject.__name__)


class AttachView(WizardStep):
    interface.implements(IContentViewStep)

    def update(self):
        super(AttachView, self).update()

        id = getUtility(IIntIds).queryId(removeAllProxies(self.context))

        self.url = '%s/@@content.attachment/%s/'%(
            absoluteURL(getSite(), self.request), id)


class FileView(object):

    def show(self):
        try:
            return self.context.data.show(
                self.request, contentDisposition=self.context.disposition)
        except:
            return u''


class ImageView(object):

    def show(self):
        try:
            return self.context.data.show(self.request)
        except:
            return u''

class MediaView(object):

    def show(self):
        try:
            return self.context.data.show(self.request)
        except:
            return u''

class AddLinkForm(AddForm):

    def nextURL(self):
        container = self.context.__parent__.__parent__
        return '%s/%s/context.html'%(
            absoluteURL(container, self.request), self._addedObject.__name__)


class LinkView(object):

    def __call__(self):
        try:
            self.request.response.redirect(self.context.url)
        except:
            pass


class AttachmentViewView(object):
    interface.implements(IContentViewView)
    component.adapts(IAttachment, interface.Interface)

    name = u'context.html'

    def __init__(self, file, request):
        pass

class AttachmentAbsoluteURL(AbsoluteURL):

    def __str__(self):
        id = getUtility(IIntIds).queryId(removeAllProxies(self.context))
        return '%s/@@content.attachment/%s'%(
            absoluteURL(getSite(), self.request), id)

    __call__ = __str__
