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
			'fieldname': 'account',
			'label': _('Account'),
			'fieldtype': 'Link',
			'options': 'Account',
			'width': 240
		},
		{
			'fieldname': 'cost_center',
			'label': _('Cost Center'),
			'fieldtype': 'Link',
			'options': 'Cost Center',
			'width': 180
		},
		{
			'fieldname': 'debit',
			'label': _('Debit'),
			'fieldtype': 'Currency',
			'width': 150
		},
		{
			'fieldname': 'credit',
			'label': _('Credit'),
			'fieldtype': 'Currency',
			'width': 140
		},
		{
			'fieldname': 'balance',
			'label': _('Balance'),
			'fieldtype': 'Currency',
			'width': 150
		}
	];

def get_data(filters):
	data = []
	company = filters.get('company')
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	from_account = filters.get('from_account')
	to_account = filters.get('to_account')
	cost_center = filters.get('cost_center')
	show_zero_values = filters.get('show_zero_values')

	root_account = from_account if from_account else frappe.db.get_all('Account', filters = { 'root_type': 'Expense', 'parent_account': '' }, pluck = 'name')[0];
	first_account_no = frappe.db.get_value('Account', root_account, 'account_number');
	last_account_no = frappe.db.get_value('Account', to_account, 'account_number') if to_account else None;
		
	def is_group(account):
		return frappe.db.get_value('Account', account, 'is_group');

	def get_pending_accounts(accounts_list):
		for account in accounts_list:
			if is_group(account):
				insert_index = accounts_list.index(account) + 1;
				child_accounts = None;
				if last_account_no:
					child_accounts = frappe.db.get_all('Account', 
						filters = { 'root_type': 'Expense', 'parent_account': account, 'account_number': ['<=', last_account_no] }, 
						or_filters = { 'root_type': 'Expense', 'parent_account': account, 'account_number': ['>=', first_account_no] },
						pluck = 'name'
					);
				else:
					child_accounts = frappe.db.get_all('Account', 
						filters = { 'root_type': 'Expense', 'parent_account': account, 'account_number': ['>=', first_account_no] }, 
						pluck = 'name'
					);
				accounts_list[ insert_index:insert_index ] = child_accounts;

		return accounts_list;

	pending_accounts = get_pending_accounts([root_account]);

	conditions = " AND gle.docstatus = 1 ";

	if company:
		conditions += f" AND gle.company = '{company}'";
	if cost_center:
		conditions += f" AND gle.cost_center = '{cost_center}'";

	def append_accounts(account, indent, conditions, from_date, to_date, from_account, to_account):
		conditions += f" AND gle.account LIKE '%{account}'"
		if is_group(account):
			parent = None if indent == 0 else frappe.db.get_value('Account', account, 'parent_account');

			data.append({ 'account': account, 'indent': indent, 'parent': parent, 'debit': 0, 'credit': 0, 'balance': 0 });
		else:
			gl_entry = frappe.db.sql(f"""
				SELECT	IFNULL(gle.account, '{account}') as "account",
						SUM(gle.credit_in_account_currency) as "credit",
						SUM(gle.debit_in_account_currency) as "debit",
						SUM(gle.debit_in_account_currency - gle.credit_in_account_currency) as "balance",
						gle.cost_center as "cost_center",
						ac.parent_account as "parent"
				FROM `tabGL Entry` as gle
				INNER JOIN `tabAccount` as ac
				ON gle.account = ac.name
				WHERE (gle.posting_date BETWEEN '{from_date}' AND '{to_date}')  {conditions}
				""", as_dict = True);

			if gl_entry:
				gl_entry = gl_entry[0];
				gl_entry['indent'] = indent;
				
				data.append(gl_entry);

				# fill credit, debit and balance for all parent accounts on the tree.
				if indent > 0:
					child_row = gl_entry;
					parent_account = child_row['parent'];

					while parent_account:
						totals_row = list(filter(lambda x: x['account'] == parent_account, data));

						if totals_row:
							totals_row = totals_row[0];
							totals_row['debit']	+= child_row['debit'];
							totals_row['credit'] += child_row['credit'];
							totals_row['balance'] += child_row['balance'];

							parent_account = totals_row['parent'];

	for account in pending_accounts:
		parent_account = frappe.db.get_value('Account', account, 'parent_account');

		parent_row = list(filter(lambda x: x['account'] == parent_account, data));

		indent = (parent_row[0]['indent']) + 1 if parent_row else 0;

		append_accounts(account, indent, conditions, from_date, to_date, from_account, to_account);

	if not show_zero_values:
		data = list(filter(lambda x: x['balance'], data));
	
	return data;

	