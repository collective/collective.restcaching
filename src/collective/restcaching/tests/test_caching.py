# -*- coding: utf-8 -*-
'''Setup tests for this package.'''
from collective.restcaching.testing import COLLECTIVE_RESTCACHING_FUNCTIONAL_TESTING  # noqa: E501
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.textfield.value import RichTextValue
from plone.caching.interfaces import ICacheSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import requests
import unittest


class TestCaching(unittest.TestCase):
    '''Test collective.restcaching.'''

    layer = COLLECTIVE_RESTCACHING_FUNCTIONAL_TESTING

    def setUp(self):
        '''Custom shared utility setup for tests.'''
        self.app = self.layer['app']
        self.request = self.layer['request']
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.registry = getUtility(IRegistry)
        self.cacheSettings = self.registry.forInterface(ICacheSettings)
        self.cacheSettings.enabled = True
        applyProfile(self.portal, 'plone.app.caching:without-caching-proxy')

    def test_vary_header(self):
        '''...'''
        # Add folder content
        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        self.portal.invokeFactory('Folder', 'f1')
        self.portal['f1'].title = u'Folder one'
        self.portal['f1'].description = u'Folder one description'
        self.portal['f1'].reindexObject()

        # Add page content
        self.portal['f1'].invokeFactory('Document', 'd1')
        self.portal['f1']['d1'].title = u'Document one'
        self.portal['f1']['d1'].description = u'Document one description'
        testText = 'Testing... body one'
        self.portal['f1']['d1'].text = RichTextValue(
            testText,
            'text/plain',
            'text/html',
        )
        self.portal['f1']['d1'].reindexObject()

        # Publish the folder and page
        self.portal.portal_workflow.doActionFor(self.portal['f1'], 'publish')
        self.portal.portal_workflow.doActionFor(
            self.portal['f1']['d1'], 'publish')

        import transaction
        transaction.commit()

        # anonymous requests
        response = requests.request(
            'GET',
            self.portal_url + '/f1/d1/',
            # Firefox
            headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'].split(';')[0], 'text/html')
        self.assertEqual(response.headers['X-Cache-Operation'], 'plone.app.caching.weakCaching')
        self.assertNotIn('Accept', response.headers.get('Vary', ''))

        # GET_application_json_
        response = requests.request(
            'GET',
            self.portal_url + '/f1/d1/',
            headers={'Accept': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertIn('Accept', response.headers.get('Vary', ''))
        self.assertEqual(response.headers['X-Cache-Operation'], 'plone.app.caching.weakCaching')
