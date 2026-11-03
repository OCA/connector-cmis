## 16.0.1.0.2

**Security**: the `password` field of `cmis.backend` is now restricted to
`base.group_system`. Internal users can no longer read it through RPC. Code
needing the password must read it with `sudo()`. `get_cmis_client` is renamed
to `_get_cmis_client` so it can no longer be called through RPC.

## 11.0.1.0.0

First official version for Odoo 11.0.
