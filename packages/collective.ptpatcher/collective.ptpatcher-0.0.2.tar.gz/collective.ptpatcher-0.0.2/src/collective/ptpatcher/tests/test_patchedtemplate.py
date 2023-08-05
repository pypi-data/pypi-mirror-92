# -*- coding: utf-8 -*-
from collective.ptpatcher.base import BasePatcher
from collective.ptpatcher.testing import COLLECTIVE_PTPATCHER_INTEGRATION_TESTING  # noqa
from lxml import etree
from plone import api
from Products.CMFPlone.browser.admin import Overview
from Products.Five import BrowserView
from pyquery import PyQuery as pq

import unittest


class DummyPatchedPTFile(BasePatcher):
    ''' Dummy patcher for testing purpose
    '''
    def get_patched(self):
        ''' A patcher that capitalizes text
        '''
        with open(self.source) as source:
            return source.read().capitalize()


patched_hello_world = DummyPatchedPTFile(
    source=('collective.ptpatcher.tests', 'templates/hello_world.pt',),
    target=('collective.ptpatcher.tests', 'ptpatcher/hello_world.pt',),
)


class DummyView(BrowserView):
    ''' A view with a patched template
    '''

    index = patched_hello_world.apply_patch().as_index()


class OverviewPatchedPTFile(BasePatcher):
    ''' Dummy patcher for testing purpose
    '''
    def get_patched(self):
        ''' A patcher that capitalizes text
        '''
        obj = pq(filename=self.source)
        header = obj('h1')[0]
        pq(header).after('<p>Sites created: ${python:len(sites)}</p>')
        return str(obj)


overview_patched = OverviewPatchedPTFile(
    source=('Products.CMFPlone.browser', 'templates/plone-overview.pt',),
    target=('collective.ptpatcher', 'tests/ptpatcher/plone-overview.pt'),
)


class PatchedOverview(Overview):
    ''' Patched Plone overview
    '''

    index = overview_patched.apply_patch().as_index()


class ColophonPatchedPTFile(BasePatcher):
    ''' Dummy patcher for testing purpose
    '''
    def get_patched(self):
        ''' A patcher that capitalizes text
        '''
        xml = etree.parse(self.source)
        new_xml = etree.XML('<strong>Test ptpatcher</strong>')
        xml.find('.//{http://www.w3.org/1999/xhtml}section').append(new_xml)
        return etree.tostring(xml)


ColophonPatchedPTFile(
    source=('Products.CMFPlone.browser', 'templates/colophon.pt',),
    target=(
        'collective.ptpatcher.tests',
        'jbot/Products.CMFPlone.browser.templates.colophon.pt',
    ),
).apply_patch()


class TestSetup(unittest.TestCase):
    '''Test that collective.ptpatcher is properly installed.'''

    layer = COLLECTIVE_PTPATCHER_INTEGRATION_TESTING

    def setUp(self):
        '''Custom shared utility setup for tests.'''
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_dummy_patch(self):
        '''Test that ICollectivePtpatcherLayer is registered.'''
        view = api.content.get_view(
            'test-ptpatcher',
            self.portal,
            self.request.clone(),
        )
        self.assertEqual(
            view(),
            u'Hello world!\n',
        )

    def test_xml_patch(self):
        view = api.content.get_view(
            'test-patched-plone-overview',
            self.app,
            self.request.clone(),
        )
        self.assertIn(
            u'<p>Sites created: 1</p>',
            view(),
        )

    def test_jbot_patch(self):
        self.assertIn(
            u'<strong>Test ptpatcher</strong>',
            self.portal(),
        )
