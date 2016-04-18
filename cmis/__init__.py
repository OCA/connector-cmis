# -*- coding: utf-8 -*-
# © 2014-2015 Savoir-faire Linux (<http://www.savoirfairelinux.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import httplib2
import functools
from . import (
    backend,
    models,
)

logger = logging.getLogger(__name__)

logger.warning('Disable SSL Certificate Validation by python code')
httplib2.Http = functools.partial(
    httplib2.Http, disable_ssl_certificate_validation=True)
