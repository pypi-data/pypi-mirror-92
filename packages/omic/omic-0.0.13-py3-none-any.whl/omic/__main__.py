#!/usr/bin/env python3
# -.- coding: utf-8 -.-
"""Omic CLI."""


from pathlib import Path
import json
import sys

from omic import omic


HERE = Path(__file__).parent
SU = '63be793a-6e1b-40cd-9f70-49dd73f470ab'


omic.configure({'user': SU})


_, cmd, *args = sys.argv
if cmd == 'search': 
    assert len(args) == 1, 'Search:  too many arguments!'
    arg, *_ = args
    client = omic.client()
    output = client.fulfill(arg)
    print()
    if isinstance(output, dict):
        print(json.dumps(output, indent=4))
    else:
        print(output)
