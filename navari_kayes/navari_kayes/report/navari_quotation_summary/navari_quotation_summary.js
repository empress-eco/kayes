// Copyright (c) 2024, Navari Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Navari Quotation Summary"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"width": "100px",
			"reqd": 1
		},
		{
			"fieldname":"start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_start_date"),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"default": frappe.defaults.get_user_default("year_end_date"),
			"reqd": 1,
			"width": "100px"
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			options: [
				{ "value": "Approved", "label": __("Approved") },
				{ "value": "Pending Approval", "label": __("Pending Approval") },
			],
		}
	]
};