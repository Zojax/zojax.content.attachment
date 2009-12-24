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
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zojax.extensions.interfaces import IExtensible

from interfaces import IImage, IAttachmentsExtension, IMedia


class Vocabulary(SimpleVocabulary):

    def getTerm(self, value):
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.by_value.keys()[0]]


class AllVocabulary(object):
    """ all attachments vocabulary """
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        while not IExtensible.providedBy(context):
            context = getattr(context, '__parent__', None)
            if context is None:
                return SimpleVocabulary(())

        extension = IAttachmentsExtension(context)

        terms = []
        for attach in extension.values():
            name = attach.__name__
            if attach.title:
                title = u'%s (%s)'%(attach.title, name)
            else:
                title = name
            terms.append((title, name, SimpleTerm(name, name, title)))

        terms.sort()
        return Vocabulary([term for t,n,term in terms])


class ImagesVocabulary(object):
    """ images vocabulary """
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        while not IExtensible.providedBy(context):
            context = getattr(context, '__parent__', None)
            if context is None:
                return SimpleVocabulary(())

        extension = IAttachmentsExtension(context)

        terms = []
        for attach in extension.values():
            if IImage.providedBy(attach) and attach.data.size:
                name = attach.__name__
                if attach.title:
                    title = u'%s (%s)'%(attach.title, name)
                else:
                    title = name
                terms.append((title, name, SimpleTerm(name, name, title)))

        terms.sort()
        return Vocabulary([term for t,n,term in terms])

class MediasVocabulary(object):
    """ medias vocabulary """
    interface.implements(IVocabularyFactory)

    def __call__(self, context):
        while not IExtensible.providedBy(context):
            context = getattr(context, '__parent__', None)
            if context is None:
                return SimpleVocabulary(())

        extension = IAttachmentsExtension(context)

        terms = []
        for attach in extension.values():
            if IMedia.providedBy(attach) and attach.data.size:
                name = attach.__name__
                if attach.title:
                    title = u'%s (%s)'%(attach.title, name)
                else:
                    title = name
                terms.append((title, name, SimpleTerm(name, name, title)))

        terms.sort()
        return Vocabulary([term for t,n,term in terms])
