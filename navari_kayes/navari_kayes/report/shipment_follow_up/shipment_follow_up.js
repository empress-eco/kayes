// Copyright (c) 2023, Navari Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Shipment Follow Up"] = {
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
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"reqd": 0,
			"width": "100px",
		},
		{
			"fieldname":"expexted_date",
			"label": __("Expexted Date"),
			"fieldtype": "Date",
			"reqd": 1,
			"width": "80px",
			"default": "__python__:from dateutil import relativedelta; from datetime import datetime; current_date + relativedelta(day=31).strftime('%Y-%m-%d')"
		},
		{
			"fieldname":"customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"reqd": 0,
			"width": "100px",
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"reqd": 0,
			"width": "100px",
		}

	]
};
