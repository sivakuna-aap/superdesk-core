# -*- coding: utf-8; -*-
#
# This file is part of Superdesk.
#
# Copyright 2013, 2014 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license


import superdesk
from bson import ObjectId
from superdesk.tests import TestCase
from superdesk.datalayer import SuperdeskJSONEncoder


class DatalayerTestCase(TestCase):

    def test_find_all(self):
        data = {'resource': 'test', 'action': 'get'}
        superdesk.get_resource_service('activity').post([data])
        self.assertEqual(1, superdesk.get_resource_service('activity').get(req=None, lookup={}).count())

    def test_json_encoder(self):
        _id = ObjectId()
        encoder = SuperdeskJSONEncoder()
        text = encoder.dumps({'_id': _id, 'name': 'foo', 'group': None})
        self.assertIn('"name": "foo"', text)
        self.assertIn('"group": null', text)
        self.assertIn('"_id": "%s"' % (_id, ), text)

    def test_find_with_mongo_query(self):
        service = superdesk.get_resource_service('activity')
        service.post([
            {'resource': 'foo', 'action': 'get'},
            {'resource': 'bar', 'action': 'post'},
        ])

        self.assertEqual(1, service.find({'resource': {'$in': ['foo']}}).count())
        self.assertEqual(1, service.find({}, max_results=1).count(True))
