{
    'name': 'ms_last_date',
    'version': '15.0.0.2',
    'summary': 'Add decoration to customer',
    'description': 'Add decoration to customer based on last transaction date and credit amount',
    'category': 'Invoicing',
    'author': "Mohamed Sobh",
    'website': 'Website',
    'license': 'LGPL-3',
    'depends': ['account', 'contacts'],
    'data': [
        'views/res_partner.xml',
    ],
    # 'demo': ['Demo'],
    'installable': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': {
        },
        'web.assets_qweb': {
        },
    },
}
