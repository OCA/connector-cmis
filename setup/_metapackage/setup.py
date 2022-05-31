import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-connector-cmis",
    description="Meta package for oca-connector-cmis Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-cmis',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
