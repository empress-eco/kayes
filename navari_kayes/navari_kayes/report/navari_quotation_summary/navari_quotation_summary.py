# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _, scrub
from pypika import Case
from functools import reduce


def execute(filters=None):
     columns = get_columns()
     data = get_quotation_data(filters)
        
     return columns, data



def get_columns():
    columns = [ 
            {
                "label": _("Start Date"),
                "fieldname": "start_date",
                "fieldtype": "Date",
                "width": 100,
            },
            {
                "label": _("End Date"),
                "fieldname": "end_date",
                "fieldtype": "Date",
                "width": 100,
            },
            {
                "label": _("Description"),
                "fieldname": "quotation_number",
                "fieldtype": "Link",
                "options": "Quotation",
                "width": 120,
            },
            {
                "label": _("Customer Name"),
                "fieldname": "customer_name",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 150,
            },
            {
                "label": _("Status"),
                "fieldname": "status",
                "fieldtype": "Data",
                "width": 100,
            },
            {
                "label": _("VAT Status"),
                "fieldname": "vat_status",
                "fieldtype": "Data",
                "width": 100,
            },
            {
                "label": _("Sales"),
                "fieldname": "sales",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": _("VAT"),
                "fieldname": "vat",
                "fieldtype": "Currency",
                "width": 100,
            },
            {
                "label": _("Total"),
                "fieldname": "total",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": _("Cost"),
                "fieldname": "cost",
                "fieldtype": "Currency",
                "width": 120,
            },
            {
                "label": _("Margin"),
                "fieldname": "margin",
                "fieldtype": "Currency",
                "width": 120,
            },
    ]

    return columns

def get_quotation_data(filters):
    company = filters.get('company')
    transaction_date = filters.get('start_date')
    valid_till = filters.get('end_date')
    status = filters.get('status')
	
    quotation = frappe.qb.DocType("Quotation")
    quotation_item = frappe.qb.DocType("Quotation Item")
    sales_taxes_charges = frappe.qb.DocType("Sales Taxes and Charges")

    conditions = [quotation.docstatus == 1]
    if company:
        conditions.append(quotation.company == company)
    if transaction_date:
        conditions.append(quotation.transaction_date == transaction_date)
    if valid_till:
        conditions.append(quotation.valid_till == valid_till)
    if status:
        conditions.append(quotation.workflow_state == status)


    query = frappe.qb.from_(quotation) \
        .inner_join(quotation_item) \
        .on(quotation_item.parent == quotation.name) \
        .inner_join(sales_taxes_charges) \
        .on(sales_taxes_charges.parent == quotation.name) \
        .select(
            quotation.transaction_date.as_("start_date"),
            quotation.valid_till.as_("end_date"),
            quotation.name.as_("quotation_number"),
            quotation.customer_name,
            Case()
            .when(quotation.workflow_state == 'Approved', 'Approved')
            .else_('Pending Approval')
            .as_('status'),
            quotation.taxes_and_charges.as_("vat_status"),
            quotation.base_total.as_("sales"),
            sales_taxes_charges.base_tax_amount.as_("vat"),
            sales_taxes_charges.base_total.as_("total"),
            quotation_item.valuation_rate.as_("cost"),
            quotation_item.gross_profit.as_("profit"),
            ((quotation_item.gross_profit / quotation.base_total) * 100).as_("margin")
        ).where(reduce(lambda x, y: x & y, conditions))

    data = query.run(as_dict=True)

    report_data = []
    for row in data:
        report_data.append({
            "start_date": row["start_date"],
            "end_date": row["end_date"],
            "quotation_number": row["quotation_number"],
            "customer_name": row["customer_name"],
            "status": row["status"],
            "vat_status": row["vat_status"],
            "sales": row["sales"],
            "vat": row["vat"],
            "total": row["total"],
            "cost": row["cost"],
            "profit": row["profit"],
            "margin": row["margin"]
        })
    return report_data

