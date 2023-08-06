#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
parsers.py
"""
import json

from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser

from humplib import json_hump2underline


DEFAULT_CHARSET = 'utf-8'


class SnakeJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        if settings.DEFAULT_CHARSET:
            encoding = settings.DEFAULT_CHARSET
        else:
            encoding = DEFAULT_CHARSET
        encoding = parser_context.get('encoding', encoding)
        try:
            data = stream.read().decode(encoding)
            data_str = json_hump2underline(data)
            return json.loads(data_str)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % str(exc))


class UnderlineParser(SnakeJSONParser):
    pass
