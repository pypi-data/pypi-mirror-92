#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Undifferentiated client; mainly user and util functionality."""


import json

from munch import munchify
import requests

from omic.client import Client
from omic.util import strict_http_do


__copyright__ = 'Copyright © 2020 Omic'


class GlobalClient(Client):

    def retrieve_project(self):
        return self._hit(
            'get',
            endpoint='/user/project'
        )

    def fulfill(self, obj: object, recurse: bool = False, s3: bool = False):
        return self._hit(
            'post',
            endpoint='/util/fulfill', 
            json_body=obj,
            qparams=self._build_args(recurse=recurse, expand_s3p=s3)
        )
