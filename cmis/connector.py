# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.addons.connector.connector import Environment
from openerp.addons.connector.checkpoint import checkpoint


def get_environment(session, model_name, cmis_backend_id):
    """ Create an environment to work with.  """
    backend_record = session.browse('cmis.backend', cmis_backend_id)
    env = Environment(backend_record, session, model_name)
    lang = backend_record.default_lang_id
    lang_code = lang.code if lang else 'en_US'
    env.set_lang(code=lang_code)
    return env


def add_checkpoint(session, model_name, record_id, cmis_backend_id):
    """ Add a row in the model ``connector.checkpoint`` for a record,
    meaning it has to be reviewed by a user.
    :param session: current session
    :type session: :class:`openerp.addons.connector.session.ConnectorSession`
    :param model_name: name of the model of the record to be reviewed
    :type model_name: str
    :param record_id: ID of the record to be reviewed
    :type record_id: int
    :param cmis_backend_id: ID of the Cmis Backend
    :type cmis_backend_id: int
    """
    return checkpoint.add_checkpoint(
        session, model_name, record_id, 'cmis.backend', cmis_backend_id)
