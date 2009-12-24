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
"""Setup for zojax.content.attachment package

$Id$
"""
import sys, os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version='1.3.4'


setup(name = 'zojax.content.attachment',
      version = version,
      author = 'Nikolay Kim',
      author_email = 'fafhrd91@gmail.com',
      description = "Content attachments.",
      long_description = (
          'Detailed Dcoumentation\n' +
          '======================\n'
          + '\n\n' +
          read('CHANGES.txt')
          ),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Zope3'],
      url='http://zojax.net/',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir = {'':'src'},
      namespace_packages=['zojax', 'zojax.content'],
      install_requires = ['setuptools', 'rwproperty', 'simplejson', 'ZODB3',
                          'zope.proxy',
                          'zope.schema',
                          'zope.component',
                          'zope.interface',
                          'zope.publisher',
                          'zope.security',
                          'zope.location',
                          'zope.datetime',
                          'zope.annotation',
                          'zope.traversing',
                          'zope.i18n',
                          'zope.i18nmessageid',
                          'zope.keyreference',
                          'zope.app.intid',
                          'zope.app.publisher',
                          'zope.app.component',

                          'z3c.schema',
                          'z3c.traverser',
                          'z3c.breadcrumb',

                          'zopyx.txng3.core',

                          'zojax.filefield',
                          'zojax.extensions',
                          'zojax.content.type',
                          'zojax.content.forms',
                          'zojax.content.permissions',
                          'zojax.ownership',
                          ],
      extras_require = dict(test=['zope.testing',
                                  'zope.testbrowser',
                                  'zope.app.testing',
                                  'zope.app.zcmlfiles',
                                  'zope.securitypolicy',
                                  'zojax.autoinclude',
                                  'zojax.personal.space',
                                  'zojax.content.space',
                                  'zojax.content.activity',
                                  'zojax.content.browser [test]',
                                  ]),
      include_package_data = True,
      zip_safe = False
      )
