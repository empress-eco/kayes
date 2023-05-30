# Copyright (c) 2023, Navari Limited and contributors
# For license information, please see license.txt

import dataclasses
import frappe
from frappe import _

def execute(filters=None):
	return get_columns, get_data(filters);

def get_columns():
	return [
	    {
			'fieldname': 'purchase_order',
			'label': _('Purchase Order'),
			'fieldtype': 'Link',
			'width': 240
		},  
		{
			'fieldname': 'depertment',
			'label': _('Depertment'),
			'fieldtype': 'Link',
			'options': 'Depertment',
			'width': 240
		},
		{
			'fieldname': 'description',
			'label': _('Description'),
			'fieldtype': 'Link',
			'options': 'Description',
			'width': 180
		},
		{
			'fieldname': 'customer_name',
			'label': _('Customer Name'),
			'fieldtype': 'Link',
			'width': 240
		},
		{
			'fieldname': 'expecterd_shipping_date',
			'label': _('Expexted Shipping Date'),
			'fieldtype': 'Date',
			'width': 140
		},
		{
			'fieldname': 'expecterd_arrival_date',
			'label': _('Expexted Arrival Date'),
			'fieldtype': 'Date',
			'width': 140
		},
		{
			'fieldname': 'shipping_terms_and_methods',
			'label': _('Shipping Terms and Methods'),
			'fieldtype': 'Link',
			'width': 150
		},
		{
			'fieldname': 'customer_delivery_destination',
			'label': _('Customer Delivery Destination'),
			'fieldtype': 'Link',
			'width': 150
		},
		{
			'fieldname': 'delivery_place',
			'label': _('Delivery Place'),
			'fieldtype': 'Link',
			'width': 150
		},
		{
			'fieldname': 'shipping_info',
			'label': _('Shipping Info'),
			'fieldtype': 'Link',
			'width': 150
		},
		{
			'fieldname': 'customer_delivery_deadline',
			'label': _('Customer Delivery Deadline'),
			'fieldtype': 'Date',
			'width': 140
		},
	];

def get_data(filters):
    data = []
    company = filters.get('company')
    supplier = filters.get('supplier')
    expected_date = filters.get('expected_date')
    customer = filters.get('customer')
    depart = filters.get('depart')

    sales_order = frappe.db.sql(f"""
        SELECT
            `tabPurchase Order Item`.parent AS purchase_order,
            `tabPurchase Order Item`.description AS department,
            `tabSales Order`.customer_name,
            `tabSales Order`.transaction_date AS expected_shipping_date,
            `tabSales Order`.delivery_date AS expected_arrival_date,
            `tabSales Order`.shipping_rule AS shipping_terms_and_methods,
            `tabSales Order`.customer_address AS customer_delivery_destination,
            `tabSales Order`.named_place AS delivery_place,
            `tabSales Order`.shipping_address_name AS shipping_info,
            `tabSales Order`.delivery_date AS customer_delivery_deadline
        FROM
            `tabSales Order`
        INNER JOIN
            `tabPurchase Order Item` ON `tabSales Order`.name = `tabPurchase Order Item`.sales_order
	    WHERE
	    (`tabSales Order`.transaction_date = (expected_date)
    """, as_dict=True)

    data.append(sales_order)
    return data

 




