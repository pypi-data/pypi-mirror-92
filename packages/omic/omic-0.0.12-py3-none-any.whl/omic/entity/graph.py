#!/usr/bin/env python3
# -.- coding: utf-8 -.-


from typing import Union
from operator import itemgetter
import json

from munch import munchify, Munch
import requests
import stackeddag.graphviz as sd  

from omic.client import Client


__copyright__ = 'Copyright © 2020 Omic'


class GraphClient(Client):

    def __init__(self, config: dict):
        self.config = config

    def retrieve(
        self, 
        _id: str = None, 
        name: str = None,
        fulfill: bool = False, 
        recurse: bool = False
    ) -> Munch:
        qparams = {} if not (_id or name) else self._build_args(**{
            '_id': _id,
            'name': name,
            'fulfill': fulfill,
            'recurse': recurse
        })
        return self._hit(
            'get',
            '/graph',
            qparams=qparams
        )

    def delete(self, graph: object) -> None:
        _id = graph if isinstance(graph, str) else graph['_id']
        self._hit('delete', '/graph', qparams={'_id': _id})

    def create(
        self,
        name: str,
        parameters: dict,
        entry: str = None, 
        structure: dict = None,
        nodes: list = [],
        labels: list = [],
        hyperparameters: dict = {},
        description: str = None,
        # TODO:  Better...
        source: str = 'dockerpal',
        meta: dict = {'label': 'recipe'}
    ) -> str:
        return self._hit(
            'post',
            '/graph',
            json_body={
                'name': name, 
                'description': description,
                'entry': entry, 
                'structure': structure,
                'parameters': parameters,
                'hyperparameters': hyperparameters,
                'nodes': nodes,
                'labels': labels,
                'source': source,
                'meta': meta
            }
        )._id

    def print(
        self,
        graph: Union[Munch, str]
    ) -> None: 
        graph = graph if not isinstance(graph, str) else self.retrieve(graph)
        # Snag graph edges
        entry, structure = itemgetter('entry', 'structure')(graph)
        edges = []
        stack = [entry]
        while len(stack):
            layer = stack.pop()
            node = structure[layer]
            next_layers = node.get('next', [])
            edges += [(layer, nl) for nl in next_layers]
            stack += next_layers
        # Convert to standard DOT format
        dot = 'graph { ' \
            + '; '.join('%s -> %s' % (a, b) for a, b in edges) \
            + ' }'
        dotfile = '/tmp/%s.dot' % graph.name
        with open(dotfile, 'w+') as f:
            f.write(dot)
        # Print DAG
        print()
        print('-' * 50)
        print(graph.name.upper(), '({})'.format(graph._id[:10]))
        if graph.description:
            print(graph.description)
        print('-' * 50)
        print()
        print(sd.fromDotFile(dotfile))
        print('-' * 50)
        print()
