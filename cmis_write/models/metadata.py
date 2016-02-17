# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm, fields


class metadata(orm.Model):
    _name = "metadata"
    _description = "Metadata"
    _columns = {
        'name': fields.char("Name", required=True, select=1, help="Name"),
        'model_id': fields.many2one(
            'ir.model',
            'Model',
            required=True,
            select=1,
            help="Model"
        ),
        'field_ids': fields.many2many(
            'ir.model.fields',
            'metadata_field_rel',
            'meta_id', 'field_id',
            'Fields',
            help="Fields"
        ),
        'metadata_list_ids': fields.one2many(
            'metadata.list',
            'metadata_id',
            'List of fields',
            help="List of fields"
        ),
        'model_ids': fields.many2many(
            'ir.model',
            string='Model List',
            help="Model List"
        ),
    }

    def onchange_model(self, cr, uid, ids, model_id, context=None):
        if context is None:
            context = {}
        if not model_id:
            return {'value': {'model_ids': [(6, 0, [])]}}
        model_ids = [model_id]
        model_obj = self.pool.get('ir.model')
        active_model_obj = self.pool.get(model_obj.browse(
            cr, uid, model_id, context=context).model)
        if active_model_obj._inherits:
            for key, val in active_model_obj._inherits.items():
                found_model_ids = model_obj.search(cr,
                                                   uid, [('model', '=', key)],
                                                   context=context)
                model_ids += found_model_ids
        return {'value': {'model_ids': [(6, 0, model_ids)]}}
