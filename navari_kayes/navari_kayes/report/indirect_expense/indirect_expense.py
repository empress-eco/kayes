# Copyright (c) 2023, Navari Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data();
	return columns, data;

def get_columns():
	return [
		{
			'fieldname': 'id',
			'label': _('ID'),
			'fieldtype': 'Link',
			'options': 'GL Entry'
		},
		{
			'fieldname': 'posting_date',
			'label': _('Posting Date'),
			'fieldtype': 'Date',
		},
		{
			'fieldname': 'transaction_date',
			'label': _('Transaction Date'),
			'fieldtype': 'Date',
		},
		{
			'fieldname': 'account',
			'label': _('Account'),
			'fieldtype': 'Link',
			'options': 'Account'
		},
		{
			'fieldname': 'party',
			'label': _('Party'),
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'fieldname': 'cost_center',
			'label': _('Cost Center'),
			'fieldtype': 'Link',
			'options': 'Cost Center'
		},
		{
			'fieldname': 'voucher_no',
			'label': _('Voucher No'),
			'fieldtype': 'Data',
			'width': 150
		}
	];

def get_data():
	return[];
