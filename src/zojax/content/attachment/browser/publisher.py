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
from zojax.content.type.interfaces import IContentContainer
from zope.app.container.interfaces import IContainer
"""

$Id$
"""
from zope import interface, component
from zope.component import getUtility
from zope.app.component.hooks import getSite
from zope.location.interfaces import ISite
from zope.traversing.browser import absoluteURL
from zope.location import LocationProxy
from zope.app.intid.interfaces import IIntIds
from zope.publisher.interfaces import NotFound, IPublishTraverse, Redirect
from z3c.traverser.interfaces import ITraverserPlugin
from zojax.content.attachment.interfaces import IAttachment, IAttachmentsExtension


class AttachmentPublisherPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        if name == u'preview':
            return LocationProxy(self.context.preview, self.context, name)
        else:
            raise NotFound(self.context, name, request)


class PreviewPublisherPlugin(object):
    interface.implements(ITraverserPlugin)

    def __init__(self, container, request):
        self.context = container
        self.request = request

    def publishTraverse(self, request, name):
        if name in self.context:
            return LocationProxy(self.context[name], self.context, name)
        else:
            # generating preview instead of NotFound error
            dimensions = name.split('x')
            image = self.context
            preview = image.generatePreview(int(dimensions[0]), int(dimensions[1]))
            return LocationProxy(self.context[name], preview, name)
            #raise NotFound(self.context, name, request)


class Attachment(object):
    interface.implements(IPublishTraverse)
    component.adapts(interface.Interface, interface.Interface)

    __name__ = 'content.attachment'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def publishTraverse(self, request, name):
        try:
            content = getUtility(IIntIds).queryObject(int(name))
        except:
            raise NotFound(self.context, name, request)

        if not ISite.providedBy(self.context):
            request.response.redirect(
                '%s/%s/%s' % (
                    absoluteURL(getSite(), request), self.__name__, name))
            return LocationProxy(content, self, name)

        if IAttachment.providedBy(content):
            return LocationProxy(content, self, name)

        raise NotFound(self.context, name, request)


class InplaceAttachment(object):
    interface.implements(IPublishTraverse)
    component.adapts(interface.Interface, interface.Interface)

    __name__ = 'content.attachment'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def publishTraverse(self, request, name):
        try:
            content = getUtility(IIntIds).queryObject(int(name))
        except:
            raise NotFound(self.context, name, request)

        if IAttachment.providedBy(content):
            return LocationProxy(content, self, name)

        raise NotFound(self.context, name, request)


class Attachments(object):
    interface.implements(IPublishTraverse)
    component.adapts(interface.Interface, interface.Interface)

    __name__ = 'content.attachments'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def publishTraverse(self, request, name):
        try:
            content = getUtility(IIntIds).queryObject(int(name))
        except:
            raise NotFound(self.context, name, request)

        if content is not None:
            ext = IAttachmentsExtension(content, None)
            if ext is not None:
                return LocationProxy(ext, content, name)

        raise NotFound(self.context, name, request)


class ContentItems(object):
    interface.implements(IPublishTraverse)
    component.adapts(interface.Interface, interface.Interface)

    __name__ = 'content.browser'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def publishTraverse(self, request, name):
        try:
            content = getUtility(IIntIds).queryObject(int(name))
        except:
            raise NotFound(self.context, name, request)
        while not IContainer.providedBy(content) and content is not None:
            content = content.__parent__

        if content is not None:
            return content
            
        raise NotFound(self.context, name, request)


class ContentById(object):
    interface.implements(IPublishTraverse)
    component.adapts(interface.Interface, interface.Interface)

    __name__ = 'content.byid'

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def publishTraverse(self, request, name):
        try:
            raise Redirect(absoluteURL(getUtility(IIntIds).queryObject(int(name), request)))
        except:
            pass
        raise NotFound(self.context, name, request)
