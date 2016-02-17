# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
###############################################################################

from openerp.tests.common import TransactionCase
from openerp.osv.orm import except_orm


class test_ir_attachment(TransactionCase):

    def setUp(self):
        super(test_ir_attachment, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.ir_attachment_model = self.registry("ir.attachment")
        self.partner_model = self.registry('res.partner')
        self.metadata_model = self.registry('metadata')
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)

        partner_id = self.partner_model.create(
            self.cr, self.uid,
            {'name': 'Test Partner',
             'email': 'test@localhost',
             'is_company': True,
             }, context=None)

        blob1 = 'blob1'
        blob1_b64 = blob1.encode('base64')

        self.vals = {
            'name': 'a1',
            'datas': blob1_b64,
            'attachment_document_ids': [(0, 0, {
                'res_model': "res.partner",
                'res_id': partner_id,
                'res_name': 'Test Partner',
            })],
        }

    def test_create_ir_attachment(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        vals['datas'] = None
        context['bool_testdoc'] = True
        ir_attachment_id = self.ir_attachment_model.create(
            cr, uid, vals, context=context)
        ir_attachment_pool = self.ir_attachment_model.browse(
            cr, uid, ir_attachment_id, context=context)

        self.assertEqual(ir_attachment_pool.name, vals['name'])

    def test_data_set(self):
        cr, uid, vals = self.cr, self.uid, self.vals.copy()
        context = self.context
        ir_attachment_id = self.ir_attachment_model.create(
            cr, uid, vals, context=context)
        result = self.ir_attachment_model._data_set(
            cr, uid, [], ir_attachment_id, '',
            'testdata'.encode('base64'), context=context)
        self.assertEqual(result, True)

    def test_data_get(self):
        cr, uid, vals = self.cr, self.uid, self.vals.copy()
        context = self.context
        vals['id_dms'] = ''
        ir_attachment_id = self.ir_attachment_model.create(
            cr, uid, vals, context=context)
        self.assertRaises(
            except_orm, self.ir_attachment_model._data_get,
            cr, uid, [ir_attachment_id], None, None, context=self.context
        )
