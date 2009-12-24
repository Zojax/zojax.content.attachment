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
""" zojax.content.attachment interfaces

$Id$
"""
from zope import schema, interface
from zope.i18nmessageid import MessageFactory
from z3c.schema.baseurl import BaseURL
from zojax.filefield.field import FileField, ImageField

_ = MessageFactory('zojax.content.attachment')


class IAttachmentContentType(interface.Interface):
    """ content type """


class IAttachment(interface.Interface):
    """ attachment """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Attachment title.'),
        default = u'',
        missing_value = u'',
        required = False)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Attachment description.'),
        default = u'',
        missing_value = u'',
        required = False)


class IFileAttachment(IAttachment):
    """ attachment with file data """

    data = FileField(
        title = _(u'Attachment'),
        required = False)


class IFile(IFileAttachment):
    """ file """

    disposition = schema.Choice(
        title = _(u'Attachment type'),
        values = ('inline', 'attachment'),
        default = 'attachment',
        required = True)


class IImage(IFileAttachment):
    """ image """

    data = ImageField(
        title = _(u'Attachment'),
        required = False)

    width = interface.Attribute('Width')
    height = interface.Attribute('Height')
    preview = interface.Attribute('Preview folder')


class IMedia(IFileAttachment):
    """ media """

    data = FileField(
        title = _(u'Media data'),
        required = False)

    mediaType = schema.TextLine(
        title = _(u'Type'),
        description = _(u'Attachment media type (extension).'),
        default = u'',
        missing_value = u'',
        required = False)

    autoplay = schema.Bool(
        title = _(u'Autoplay'),
        description = _(u'Attachment media autoplay.'),
        default = True,
        required = True)

    preview = interface.Attribute('Preview folder')


class IPreviewFolder(interface.Interface):
    """ folder for image previews """

    def clear():
        """ clear previews """

    def generatePreview(width, height):
        """ generate preview """


class ILink(IAttachment):
    """ link interface """

    title = schema.TextLine(
        title = _(u'Title'),
        description = _(u'Link title.'),
        default = u'',
        required = True)

    description = schema.Text(
        title = _(u'Description'),
        description = _(u'Link description.'),
        default = u'',
        required = False)

    url = BaseURL(
        title = _(u'URL'),
        description = _(u'Link URL.'),
        required = True)


class IAttachmentsAware(interface.Interface):
    """Marker interface for content that supports attachments."""


class IAttachmentsExtension(interface.Interface):
    """ content attachments extension """
