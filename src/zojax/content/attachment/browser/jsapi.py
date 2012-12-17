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
from zope.dublincore.interfaces import IDCTimes
from zojax.filefield.data import FileData
from zojax.content.type.interfaces import IContentType, IContentContainer, IItem
from zope.app.container.interfaces import IContainer
from zope.security.management import checkPermission
"""

$Id$
"""
import os.path
import datetime
from simplejson import JSONEncoder, loads

import transaction
from zope import interface, event
from zope.proxy import removeAllProxies
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.traversing.browser import absoluteURL
from zope.lifecycleevent import ObjectCreatedEvent
from zope.app.component.hooks import getSite
from zope.app.container.interfaces import INameChooser
from zope.app.intid.interfaces import IIntIds

from zojax.content.attachment.image import Image
from zojax.content.attachment.media import Media
from zojax.content.attachment.interfaces import IImage, IMedia
from zope.app.component.hooks import getSite

from zojax.filefield.data import getImageSize
from zojax.filefield.interfaces import NotAllowedFileType


class Encoder(JSONEncoder):

    def encode(self, *kv, **kw):
        return unicode(super(Encoder, self).encode(*kv, **kw))

encoder = JSONEncoder()


def jsonable(func):

    def cal(self):
        self.request.response.setHeader('Content-Type', ' application/json')
        return unicode(func(self)).encode('utf-8')
    return cal


class IImageManagerAPI(interface.Interface):
    pass


class IMediaManagerAPI(interface.Interface):
    pass


class IContentManagerAPI(interface.Interface):
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


class ContentManagerAPI(BrowserView):
    interface.implements(IContentManagerAPI)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    def publishTraverse(self, request, name):
        view = queryMultiAdapter((self, request), name=name)
        if view is not None:
            return view

        raise NotFound(self, name, request)


class Images(object):
    
    iface = IImage

    @jsonable
    def __call__(self):
        ids = getUtility(IIntIds)
        request = self.request
        container = self.context.context
        siteUrl = absoluteURL(getSite(), request)

        try:
            start = int(self.request.form.get('start', '0'))
        except (TypeError, ValueError), e:
            start = 0
        try:
            limit = int(self.request.form.get('limit', '0'))
        except (TypeError, ValueError), e:
            limit = 0

        try:
            width = int(request.form.get('pw', 150))
        except:
            width = 150

        try:
            height = int(request.form.get('ph', 150))
        except:
            height = 150
        
        sort = self.request.form.get('sort', 'modified')
        sort_direction = self.request.form.get('dir', 'DESC').upper()
        
        data = []
        for name, image in container.items():
            if self.iface.providedBy(image) and image.data is not None:
                id = ids.queryId(removeAllProxies(image))
                removeAllProxies(image.preview).generatePreview(width, height)
                info = {'id': id,
                        'name': image.__name__,
                        'title': image.title or image.__name__,
                        'width': image.width,
                        'height': image.height,
                        'size': len(image.data),
                        'modified': IDCTimes(image).modified.isoformat()[:19].replace('T',' '),
                        'url': '@@content.attachment/%s'%id,
                        'preview': '%s/content.attachment/%s/preview/%sx%s/'%(siteUrl, id, width, height),
                        }
                data.append(info)

        data.sort(key=lambda x: x[sort], reverse=sort_direction == 'DESC')
        return encoder.encode({'images': data[start:limit and start+limit or None], 'total': len(data)})


class FileUpload(object):

    @jsonable
    def __call__(self):
        request = self.request
        container = self.context.context
        image = request.form.get('file', '')

        if not image:
            return encoder.encode({'success': False, 'message': '', 'error': 'No image provided'})
        name = os.path.split(image.filename)[-1]

        image = FileData(image)

        chooser = INameChooser(container)

        content = Image()

        name = chooser.chooseName(name, content)
        event.notify(ObjectCreatedEvent(content))
        container[name] = content
        try:
            content.data = image
        except NotAllowedFileType:
            transaction.abort()
            return encoder.encode({'success': False, 'message': '', 'error': 'File is not image'})
        return encoder.encode(
            {'success': True, 'message': '', 'file': name})


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

        return encoder.encode({'success': True, 'message': ''})


class Medias(object):

    @jsonable
    def __call__(self):
        ids = getUtility(IIntIds)
        request = self.request
        container = self.context.context
        siteUrl = absoluteURL(getSite(), request)
        try:
            start = int(self.request.form.get('start', '0'))
        except (TypeError, ValueError), e:
            start = 0
        try:
            limit = int(self.request.form.get('limit', '0'))
        except (TypeError, ValueError), e:
            limit = 0
        try:
            width = int(request.form.get('pw', 150))
        except:
            width = 150
        sort = self.request.form.get('sort', 'modified')
        sort_direction = self.request.form.get('dir', 'DESC').upper()
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
                        'modified': IDCTimes(media).modified.isoformat()[:19].replace('T',' '),
                        'url': '@@content.attachment/%s'%id,
                        'preview': '%s/content.attachment/%s/preview/%sx%s/'%(
                           siteUrl, id, width, height),
                        }
                data.append(info)

        data.sort(key=lambda x: x[sort], reverse=sort_direction == 'DESC')
        return encoder.encode({'medias': data[start:limit and start+limit or None], 'total': len(data)})


class MediaFileUpload(object):

    @jsonable
    def __call__(self):
        request = self.request
        container = self.context.context
        media = request.form.get('image', '')
        description = request.form.get('description', '')
        if not media:
            return encoder.encode({'success': False, 'message': '',  'error': 'No file provided'})

        name = os.path.split(media.filename)[-1]

        title = request.form.get('title', name)

        mediaType = request.form.get('type', '')

        autoplay = request.form.get('autoplay', IMedia['autoplay'].default)

        if not mediaType:
            mediaType = os.path.splitext(name)[1][1:]

        content = container.get(name)
        self.request.response.setHeader('content-type', 'text/html')
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
            return encoder.encode({'success': True, 'message': '', 'file': name})
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
            {'success': True, 'message': '', 'file': name})


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

        return encoder.encode({'success': True, 'message': ''})


class ContentItems(object):

    @jsonable
    def __call__(self):
        ids = getUtility(IIntIds)
        request = self.request
        node = request.form.get('node', 'root')
        site = getSite()
        container = site
        try:
            container = ids.getObject(int(node))
        except (TypeError, KeyError, ValueError), e:
            pass
        siteUrl = absoluteURL(site, request)
        data = []
        for name, content in IContainer(container, {}).items():
            id = ids.queryId(removeAllProxies(content))
            content = IItem(content, None)
            if content is None or not checkPermission('zope.View', content):
                continue
            info = {'id': id,
                    'text': content.title or content.__name__,
                    'description': content.description,
                    'cls': IContainer.providedBy(content) and 'folder' or 'file',
                    'leaf': not bool(IContainer.providedBy(content) and len(content)),
                    'type': getattr(IContentType(content, None), 'name', 'content'),
                    'modified': getattr(IDCTimes(content, None),'modified', datetime.datetime.now()).isoformat()[:19].replace('T',' '),
                    'url': '@@content.byid/%s'%id
                    }
            data.append((content.title, content.__name__, info))

        data.sort()
        return encoder.encode([info for t,n,info in data])
