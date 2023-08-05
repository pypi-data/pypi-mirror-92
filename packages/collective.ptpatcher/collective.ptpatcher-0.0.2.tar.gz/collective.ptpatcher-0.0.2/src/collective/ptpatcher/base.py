# coding=utf-8
from logging import getLogger
from pkg_resources import resource_filename
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import os
import six


class BasePatcher(object):

    logger = getLogger(__name__)

    def __init__(self, source, target):
        ''' Base class for pathcing templates
        '''
        if isinstance(source, tuple):
            source = resource_filename(*source)
        if isinstance(target, tuple):
            target = resource_filename(*target)
        self.source = source
        self.target = target

    @property
    def name(self):
        ''' Used for logging
        '''
        return self.__class__

    def as_index(self, *args, **kwargs):
        ''' Return the view page template file to be used as an index
        '''
        if not os.path.exists(self.target):
            self.apply_patch()
        return ViewPageTemplateFile(self.target)

    def get_patched(self):
        ''' The method used for patching
        '''
        raise RuntimeError('Not implemented yet')

    def apply_patch(self):
        ''' Path orginal and save it to target
        '''
        self.logger.info(
            '%r:\n\tSource:\t%s\n\tTarget:\t%s',
            self.name,
            self.source,
            self.target,
        )
        path = os.path.split(self.target)[0]
        if not os.path.exists(path):
            os.makedirs(path)
        with open(self.target, 'w') as ou:
            if six.PY2:
                ou.write(self.get_patched())
            else:
                ou.write(self.get_patched().decode("utf8"))
        return self
