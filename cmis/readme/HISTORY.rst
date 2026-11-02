12.0.1.0.2
~~~~~~~~~~

**Security**: internal users (``base.group_user``) no longer have read access
on ``cmis.backend``. The backend credentials (username / password) were
readable by any logged user through RPC. Only ``base.group_system`` can now
access the model.

**Breaking change**: code accessing ``cmis.backend`` on behalf of non-admin
users must use ``sudo()``.


11.0.1.0.0
~~~~~~~~~~

First official version for Odoo 11.0.
