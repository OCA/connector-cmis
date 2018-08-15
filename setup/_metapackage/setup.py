import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-connector-cmis",
    description="Meta package for oca-connector-cmis Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-cmis',
        'odoo10-addon-cmis_stock_production_lot',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
