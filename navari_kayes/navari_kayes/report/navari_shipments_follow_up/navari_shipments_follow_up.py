# Copyright (c) 2023, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"));
	return get_columns(), get_data(filters);

def get_columns():
	return [
		{
			'fieldname': 'purchase_order',
			'label': _('PO #'),
			'fieldtype': 'Link',
			'options': 'Purchase Order',
			'width': 200
		},
		{
			'fieldname': 'cost_center',
			'label': _('Dept'),
			'fieldtype': 'Link',
			'options': 'Cost Center',
			'width': 200
		},
		{
			'fieldname': 'description',
			'label': _('Description'),
			'fieldtype': 'Data',
			'width': 240
		},
		{
			'fieldname': 'supplier',
			'label': _('Supplier'),
			'fieldtype': 'Link',
			'options': 'Supplier',
			'width': 200
		},
		{
			'fieldname': 'expected_shipping_date',
			'label': _('Expected Shipping Date'),
			'fieldtype': 'Date',
			'width': 200
		},
		{
			'fieldname': 'expected_arrival_date',
			'label': _('Expected Arrival Date'),
			'fieldtype': 'Date',
			'width': 200
		},
		{
			'fieldname': 'shipping_terms_and_method',
			'label': _('Shipping Terms/Method'),
			'fieldtype': 'Link',
			'options': 'Incoterm',
			'width': 200
		},
		{
			'fieldname': 'customer_name',
			'label': _('Customer Name'),
			'fieldtype': 'Link',
			'options': 'Customer',
			'width': 240
		},
		{
			'fieldname': 'delivery_place',
			'label': _('Delivery Place'),
			'fieldtype': 'Link',
			'options': 'Address',
			'width': 150
		},
		{
			'fieldname': 'shipping_info',
			'label': _('Shipping Info'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'customer_delivery_deadline',
			'label': _('Customer Delivery Deadline'),
			'fieldtype': 'Date',
			'width': 200
		},
		{
			'fieldname': 'comments',
			'label': _('Comments'),
			'fieldtype': 'Data',
			'width': 150
		}
	];

def get_data(filters):
	company = filters.get('company');
	from_date = filters.get('from_date');
	to_date = filters.get('to_date');
	purchase_order = filters.get('purchase_order');
	supplier = filters.get('supplier');
	customer = filters.get('customer');
	cost_center = filters.get('cost_center');

	conditions = " AND 1 = 1 ";

	if company:
		conditions += f" AND po.company = '{company}'";
	if purchase_order:
		conditions += f" AND po.name = '{purchase_order}'";
	if supplier:
		conditions += f" AND  po.supplier = '{supplier}'";
	if cost_center:
		conditions += f" AND poi.cost_center = '{cost_center}'";
	if customer:
		conditions += f" AND po.customer = '{customer}'";

	shipment_details = frappe.db.sql(f"""
		SELECT po.name as purchase_order,
			po.supplier as supplier,
			po.named_place as shipping_terms_and_method,
			poi.cost_center as cost_center,
			poi.description as description,
			poi.schedule_date as expected_arrival_date,
			poi.sales_order as sales_order,
			poi.sales_order_item as sales_order_item,
			so.shipping_address_name as delivery_place,
			so.shipping_info as shipping_info
		FROM `tabPurchase Order` as po
		INNER JOIN `tabPurchase Order Item` as poi ON po.name = poi.parent
		LEFT JOIN `tabSales Order` as so ON poi.sales_order = so.name
		WHERE (po.transaction_date BETWEEN '{from_date}' AND '{to_date}') {conditions}
	""", as_dict = True);

	if shipment_details:
		for row in shipment_details:
			if row.get('sales_order_item'):
				row['expected_shipping_date'] = frappe.db.get_value('Sales Order Item', row.get('sales_order_item'), 'delivery_date');
			if row.get('sales_order'):
				row['customer_delivery_deadline'] = frappe.db.get_value('Sales Order', row.get('sales_order'), 'delivery_date');
				row['comments'] = frappe.db.get_value('Sales Order', row.get('sales_order'), 'comments');
				row['customer_name'] = frappe.db.get_value('Sales Order', row.get('sales_order'), 'customer');
				if not row.get('shipping_terms_and_method'):
					row['shipping_terms_and_method'] = frappe.db.get_value('Sales Order', row.get('sales_order'), 'named_place');
		return shipment_details;
	else:
		return [];