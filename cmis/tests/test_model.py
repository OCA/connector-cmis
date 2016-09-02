# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class test_model(TransactionCase):

    def setUp(self):
        super(test_model, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        self.user_model = self.registry("res.users")

        # Get registries
        self.model = self.registry("cmis.backend")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)

        self.vals = {
            'name': "Test cmis",
            'version': '1.0',
            'location': "http://localhost:8081/alfresco/s/cmis",
            'username': 'admin',
            'password': 'admin',
            'initial_directory_write': '/',
        }

    def test_create_model(self):
        model_id = self.model.create(
            self.cr, self.uid, self.vals, context=self.context)
        self.assertTrue(model_id)
