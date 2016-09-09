# -*- coding: utf-8 -*-
# © 2016 ACSONE SA/NV (<http://acsone.eu>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import UserError


class CMISError(UserError):
    """CMIS Error!"""
    def __init__(self, value):
        super(CMISError, self).__init__(value)
