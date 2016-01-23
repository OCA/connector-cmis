# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.tests.common import TransactionCase


class test_ir_attachment_dms_wizard(TransactionCase):

    def setUp(self):
        super(test_ir_attachment_dms_wizard, self).setUp()
        # Clean up registries
        self.registry('ir.model').clear_caches()
        self.registry('ir.model.data').clear_caches()
        # Get registries
        self.user_model = self.registry("res.users")
        self.attachment_dms_wizard_model = self.registry(
            "ir.attachment.dms.wizard")
        # Get context
        self.context = self.user_model.context_get(self.cr, self.uid)
        self.vals = {
            'name': 'TEST',
            'attachment_ids': [(0, 0, {
                'name': 'TEST',
                'file_id': 1,
                'selectable_ok': True,
            })],
        }

    def test_create_ir_attachment_dms_wizard(self):
        cr, uid, vals, context = self.cr, self.uid, self.vals, self.context
        dms_wizard_id = self.attachment_dms_wizard_model.create(
            cr, uid, vals, context=context)
        dms_wizard_obj = self.attachment_dms_wizard_model.browse(
            cr, uid, dms_wizard_id, context=context)
        self.assertEqual(dms_wizard_obj.name, vals['name'])
        self.assertEqual(dms_wizard_obj.attachment_ids[0].name, 'TEST')
