# -*- coding: utf-8 -*-
from plone.rest.interfaces import IAPIRequest


# XXX: do not works

def mark_vary_accept(event):
    """ TODO: pull request for plone.rest
    """
    request = event.request
    if IAPIRequest.providedBy(request):
        request.response.appendHeader('Vary', 'Accept')
