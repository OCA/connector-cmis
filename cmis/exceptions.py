# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.exceptions import UserError
from openerp.tools.translate import _


class CMISError(UserError):
    """CMIS Error!"""
    def __init__(self, value):
         super(CMISError, self).__init__(value)


class CMISConnectionError(CMISError):
    """CMIS connection Error!"""
    def __init__(self, value):
         super(CMISConnectionError, self).__init__(value)