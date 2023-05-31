# Copyright (c) 2023, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	return get_columns(), get_data(filters)

def get_data(filters):
	print(f"\n\n\n{filters}\n\n\n\n")

	sales_order = frappe.db.sql("""
	   SELECT
            `tabPurchase Order Item`.name AS purchase_order,
            `tabPurchase Order Item`.cost_center,
            `tabPurchase Order Item`.description,
            `tabPurchase Order`.supplier,
            `tabPurchase Order`.transaction_date AS expected_shipping_date,
            `tabPurchase Order`.schedule_date AS expected_arrival_date,
            `tabSales Order`.shipping_rule AS shipping_terms_and_methods,
            `tabSales Order`.customer_address AS customer_delivery_destination,
            `tabSales Order`.named_place AS delivery_place,
            `tabSales Order`.shipping_address_name AS shipping_info,
            `tabSales Order`.delivery_date, DATE_ADD(delivery_date, INTERVAL 2 DAY) AS customer_delivery_deadline
        FROM ((
            `tabPurchase Order Item`
        INNER JOIN
            `tabSales Order` ON `tabPurchase Order Item`.sales_order = `tabSales Order`.name)
        INNER JOIN
            `tabPurchase Order` ON `tabPurchase Order Item`.parent = `tabPurchase Order`.name);
	""")
	return sales_order	

def get_columns():
	return [
		{
			'fieldname': 'purchase_order',
			'label': _('Purchase Order'),
			'fieldtype': 'Data',
			'width': 240
		},  
		{
			'fieldname': 'cost_center',
			'label': _('Cost Center'),
			'fieldtype': 'Link',
			'options': 'Cost Center',
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
			'fieldname': 'supplier',
			'label': _('Supplier'),
			'fieldtype': 'Link',
			'options': 'Supplier',
			'width': 180
		},
		{
			'fieldname': 'expected_shipping_date',
			'label': _('Expected Shipping Date'),
			'fieldtype': 'Date',
			'width': 140
		},
		{
			'fieldname': 'expected_arrival_date',
			'label': _('Expected Arrival Date'),
			'fieldtype': 'Date',
			'width': 140
		},
		{
			'fieldname': 'shipping_terms_and_methods',
			'label': _('Shipping Terms and Methods'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'customer_delivery_destination',
			'label': _('Customer Delivery Destination'),
			'fieldtype': 'Link',
			'options': 'Customer Delivery Destination',
			'width': 150
		},
		{
			'fieldname': 'delivery_place',
			'label': _('Delivery Place'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'shipping_info',
			'label': _('Shipping Info'),
			'fieldtype': 'Link',
			'options': 'Shipping Info',
			'width': 150
		},
		{
			'fieldname': 'customer_delivery_deadline',
			'label': _('Customer Delivery Deadline'),
			'fieldtype': 'Date',
			'width': 140
		}
     
	]
