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
from zope import interface, schema
from zope.proxy import removeAllProxies
from zojax.layoutform import button, Fields, PageletAddForm
from zojax.layoutform.interfaces import ISaveAction
from zojax.wizard import WizardStepForm
from zojax.content.attachment.interfaces import _
from zojax.statusmessage.interfaces import IStatusMessage


class IPreviewForm(interface.Interface):

    width = schema.Int(
        title = _(u'Width'),
        min = 0,
        required = True)

    height = schema.Int(
        title = _(u'Height'),
        min = 0,
        required = True)


class Previews(WizardStepForm):

    buttons = WizardStepForm.buttons.copy()
    handlers = WizardStepForm.handlers.copy()

    label = _('Preview')
    fields = Fields(IPreviewForm)
    ignoreContext = True

    def isComplete(self):
        return True

    @button.buttonAndHandler(_(u'Generate'))
    def handlePreview(self, action):
        pass

    def update(self):
        super(Previews, self).update()

        if 'form.remove' in self.request:
            removed = False
            preview = removeAllProxies(self.context.preview)
            names = self.request.get('preview', ())
            for name in names:
                if name in preview:
                    del preview[name]
                    removed = True

            if removed:
                IStatusMessage(self.request).add(_('Previews have been removed.'))

        if 'previews.buttons.generate' in self.request:
            data, errors = self.extractData()

            if errors:
                IStatusMessage(self.request).add(self.formErrorsMessage, 'error')
            else:
                context = self.context
                context.preview.generatePreview(data['width'], data['height'])
                IStatusMessage(self.request).add(_('Preview has been generated.'))
