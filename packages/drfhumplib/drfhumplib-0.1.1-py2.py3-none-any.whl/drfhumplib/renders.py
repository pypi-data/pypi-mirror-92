#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
renders.py
"""

from rest_framework.renderers import JSONRenderer
from humplib import underline2hump


class HumpJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        resp = super(HumpJSONRenderer, self).render(
            data, accepted_media_type=accepted_media_type,
            renderer_context=renderer_context
        )
        resp_hump = underline2hump(resp)
        return resp_hump
