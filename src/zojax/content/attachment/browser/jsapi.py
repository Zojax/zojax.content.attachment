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
import os.path
from simplejson import JSONEncoder

import transaction
from zope import interface, event
from zope.proxy import removeAllProxies
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.traversing.browser import absoluteURL
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.content.attachment.image import Image
from zojax.content.attachment.media import Media
from zojax.content.attachment.interfaces import IImage, IMedia
from zope.app.component.hooks import getSite


class Encoder(JSONEncoder):

    def encode(self, *kv, **kw):
        return unicode(super(Encoder, self).encode(*kv, **kw))

encoder = JSONEncoder()


def jsonable(func):

    def cal(self):
        self.request.response.setHeader('Content-Type', 'text/html')
        return unicode(func(self))

    return cal


class IImageManagerAPI(interface.Interface):
    pass


class IMediaManagerAPI(interface.Interface):
    pass


class ImageManagerAPI(BrowserView):
    interface.implements(IImageManagerAPI)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context.context

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        raise NotFound(self, name, request)


class MediaManagerAPI(BrowserView):
    interface.implements(IMediaManagerAPI)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context.context

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        raise NotFound(self, name, request)


class Images(object):

    @jsonable
    def __call__(self):
        ids = getUtility(IIntIds)
        request = self.request
        container = self.context.context
        siteUrl = absoluteURL(getSite(), request)

        try:
            width = int(request.form.get('pw', 150))
        except:
            width = 150

        try:
            height = int(request.form.get('ph', 150))
        except:
            height = 150

        data = []
        for name, image in container.items():
            if IImage.providedBy(image) and image:
                id = ids.queryId(removeAllProxies(image))
                removeAllProxies(image.preview).generatePreview(width, height)

                info = {'id': id,
                        'name': image.__name__,
                        'title': image.title or image.__name__,
                        'width': image.width,
                        'height': image.height,
                        'size': len(image.data),
                        'url': '@@content.attachment/%s'%id,
                        'preview': '%s/content.attachment/%s/preview/%sx%s/'%(
                               siteUrl, id, width, height),
                        }
                data.append((image.title, image.__name__, info))

        data.sort()
        return encoder.encode({'images': [info for t,n,info in data]})


class FileUpload(object):

    @jsonable
    def __call__(self):
        request = self.request
        container = self.context.context
        image = request.form.get('image', '')

        if not image:
            return encoder.encode({'success': 'false', 'message': ''})

        name = os.path.split(image.filename)[-1]

        content = container.get(name)
        if IImage.providedBy(content):
            field = IImage['data'].bind(content)
            field.set(content, image)
            return encoder.encode({'success': 'true', 'message': ''})
        elif name in container:
            del container[name]

        content = Image()
        event.notify(ObjectCreatedEvent(content))
        container[name] = content
        field = IImage['data'].bind(content)
        field.set(content, image)
        return encoder.encode(
            {'success': 'true', 'message': '', 'file': image.filename})


class FileRemove(object):

    @jsonable
    def __call__(self):
        request = self.request
        container = self.context.context

        items = request.form.get('image', ())
        if isinstance(items, basestring):
            items = (items,)

        for name in items:
            if name in container:
                del container[name]

        return encoder.encode({'success': 'true', 'message': ''})


class Medias(object):

    @jsonable
    def __call__(self):
        ids = getUtility(IIntIds)
        request = self.request
        container = self.context.context
        siteUrl = absoluteURL(getSite(), request)

        try:
            width = int(request.form.get('pw', 150))
        except:
            width = 150

        try:
            height = int(request.form.get('ph', 150))
        except:
            height = 150

        data = []
        for name, media in container.items():
            if IMedia.providedBy(media) and media:
                id = ids.queryId(removeAllProxies(media))
                removeAllProxies(media.preview).generatePreview(width, height)

                info = {'id': id,
                        'name': media.__name__,
                        'title': media.title or media.__name__,
                        'description': media.description,
                        'type': media.mediaType,
                        'autoplay': media.autoplay,
                        'size': len(media.data),
                        'url': '@@content.attachment/%s'%id,
                        'preview': '%s/content.attachment/%s/preview/%sx%s/'%(
                           siteUrl, id, width, height),
                        }
                data.append((media.title, media.__name__, info))

        data.sort()
        return encoder.encode({'medias': [info for t,n,info in data]})


class MediaFileUpload(object):

    @jsonable
    def __call__(self):
        request = self.request
        container = self.context.context
        media = request.form.get('image', '')
        description = request.form.get('description', '')
        if not media:
            return encoder.encode({'success': 'false', 'message': ''})

        name = os.path.split(media.filename)[-1]

        title = request.form.get('title', name)

        mediaType = request.form.get('type', '')

        autoplay = request.form.get('autoplay', IMedia['autoplay'].default)

        if not mediaType:
            mediaType = os.path.splitext(name)[1][1:]

        content = container.get(name)
        if IMedia.providedBy(content):
            field = IMedia['data'].bind(content)
            field.set(content, media)
            field = IMedia['mediaType'].bind(content)
            field.set(content, mediaType)
            field = IMedia['autoplay'].bind(content)
            field.set(content, autoplay)
            field = IMedia['title'].bind(content)
            field.set(content, title)
            field = IMedia['description'].bind(content)
            field.set(content, description)
            return encoder.encode({'success': 'true', 'message': ''})
        elif name in container:
            del container[name]
        content = Media()
        event.notify(ObjectCreatedEvent(content))
        container[name] = content
        field = IMedia['data'].bind(content)
        field.set(content, media)
        field = IMedia['mediaType'].bind(content)
        field.set(content, mediaType)
        field = IMedia['autoplay'].bind(content)
        field.set(content, autoplay)
        field = IMedia['title'].bind(content)
        field.set(content, title)
        field = IMedia['description'].bind(content)
        field.set(content, description)
        return encoder.encode(
            {'success': 'true', 'message': '', 'file': media.filename})


class MediaFileRemove(object):

    @jsonable
    def __call__(self):
        request = self.request
        container = self.context.context

        items = request.form.get('media', ())
        if isinstance(items, basestring):
            items = (items,)

        for name in items:
            if name in container:
                del container[name]

        return encoder.encode({'success': 'true', 'message': ''})
