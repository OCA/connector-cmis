# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.connector.connector import Binder
from ..backend import cmis


@cmis
class CmisModelBinder(Binder):

    _model_name = []
    _external_field = 'dms_id'
    _backend_field = 'backend_id'
