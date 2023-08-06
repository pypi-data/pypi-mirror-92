#!/usr/bin/env python3
# -.- coding: utf-8 -.-

from pathlib import Path
import functools
import json
import os

from munch import munchify, Munch
import requests

from omic.client import Client
from omic.global_ import GlobalClient
from omic.parallel import run_parallel 
from omic.util import strict_http_do, check_args, get_cloud, \
                      download_url


__copyright__ = 'Copyright © 2020 Omic'


class EnvironmentClient(Client):
    def __init__(self, config: dict):
        self.config = config

    def create(
        self, 
        alias: str,
        name: str = None,
        description: str = None,
        dockerfile: str = None,
        url: str = None,
        logo: str = None 
    ):
        name = name or alias
        body = self._build_args(**{
            'alias': alias,
            'name': name,
            'description': description,
            'dockerfile': dockerfile,
            'url': url,
            'logo': logo
        })
        return self._hit(
            'post',
            endpoint='/environment',
            json_body=body,
        )._id

    def retrieve(
        self, 
        _id: str = None,
        name: str = None
    ):
        return self._hit(
            'get',
            endpoint='/environment',
            qparams=self._build_args(_id=_id, name=name)
        )

    def delete(
        self, 
        _id: str
    ):
        return self._hit(
            'delete',
            endpoint='/environment',
            qparams={'_id': _id}
        )

    def update_status(
        self, 
        env: object,
        status: str
    ) -> str:
        if not isinstance(env, str):
            env = env['_id']
        return self._hit(
            'post',
            endpoint='/environment/{_id}/status'.format(_id=env),
            json_body={'status': status}
        )
