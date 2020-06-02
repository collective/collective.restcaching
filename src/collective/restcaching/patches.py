# -*- coding: utf-8 -*-
from plone.app.caching.operations import utils


def getRAMCacheKey(request, etag=None, lastModified=None):
    """Add Vary-ation headers in cache key
    """
    resourceKey = utils._old_getRAMCacheKey(request, etag=etag, lastModified=lastModified)
    for header in request.response.getHeader('Vary', '').split(','):
        value = request.getHeader(header)
        if value:
            resourceKey = '|{header}:{value}|{resourceKey}'.format(
                header=header, value=value, resourceKey=resourceKey)
    return resourceKey
