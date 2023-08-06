#!/usr/bin/env python3
# -.- coding: utf-8 -.-


import json

from munch import munchify, Munch
import requests

from omic.client import Client


__copyright__ = 'Copyright © 2020 Omic'


class ClinicalClient(Client):

    def parse_query(
        self,
        query: str
    ) -> str:
        return self._hit(
            'post',
            '/clinical/query',
            json_body=query
        )
