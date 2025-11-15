# -*- coding: utf-8 -*-
{
    'name': "Taller",
    'summary': "Gestión de asistencia y servicios de taller en documentos de venta y facturas",
    'description': """
        Extensiones para pedidos de venta, clientes y facturación orientadas a talleres y servicios
        de asistencia vehicular en Odoo 18.
    """,
    'author': "alvpercam",
    'website': "https://www.yourcompany.com",
    'category': 'Sales/Sales',
    'version': '19.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale_management',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/partner.xml',
        'views/sale.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}
