{
    'name': 'Partner Sequence',
    'version': '1.0',
    'category': 'Custom',
    'description': """Use the standard reference field on partner for the unique partner number. Adds
    extra sequence type: Partner and a sequence with code res.partner. As default this sequence will be
    used to assign to partners. You can use the Partner Sequence forms to set different sequence for a country.
    The partner number will be added to the partner just like with the Products in ODOO.""",
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'depends': [
        'base',        
               ],
    'data': ['partner_view.xml',
             'partner_sequence.xml',
        ],
    'installable': True,
    'application': True,
    }
