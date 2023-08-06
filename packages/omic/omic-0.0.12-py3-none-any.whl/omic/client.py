#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Client base class."""


import json
import os
import urllib

from munch import munchify, Munch
import requests

from .util import strict_http_do


__copyright__ = 'Copyright © 2020 Omic'


class Client:
    def __init__(self, config: dict):
        self.config = config

    def _build_args(self, **kwargs):
        return {k: v for k, v in kwargs.items() if v}

    def _encode_qparams(self, qparams: dict) -> dict:
        """Encode dict-like query params, where the decoder resides in the API."""
        new_qparams = {}
        for k, v in qparams.items():
            if isinstance(v, dict):
                print('v', v)
                v = urllib.parse.quote(json.dumps(v))
            new_qparams[k] = v
        return new_qparams 

    def _hit(
        self, 
        method: str, 
        endpoint: str, 
        qparams: dict = {}, 
        headers: dict = {}, 
        json_body: dict = None, 
        retry_count: int = 2,
        silent: bool = True
    ) -> Munch:
        """Abstraction on all HTTP methods with our API."""
        if endpoint.startswith('/'):
            endpoint = os.path.join(self.config.endpoint, endpoint[1:]) 
        qparams.update({'user': self.config.user})
        headers.update({'x-api-key': self.config.key})
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'delete': requests.delete,
        }
        qparams = self._encode_qparams(qparams)
        methodf = method_map[method.lower()]
        if not silent:
            print('—' * 100)
            print('Hitting {} ({}):'.format(endpoint, method))
            print('Parameters:', json.dumps(qparams, indent=4))
            print('Body:', json.dumps(json_body, indent=4))
            print('—' * 100)
        return strict_http_do(lambda: methodf(endpoint, params=qparams,
                                              headers=headers, json=json_body),
                              n=retry_count)
