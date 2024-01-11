# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from pypika import Case, Criterion

def execute(filters=None):
     columns = get_columns()
     data = get_quotation_data(filters)
        
     return columns, data

def get_columns():
    columns = [ 
            {
                "label": _("Description"),
                "fieldname": "quotation_number",
                "fieldtype": "Link",
                "options": "Quotation",
                "width": 240,
            },
            {
                "label": _("Start Date"),
                "fieldname": "start_date",
                "fieldtype": "Date",
                "width": 150,
            },
            {
                "label": _("Valid Till"),
                "fieldname": "valid_till",
                "fieldtype": "Date",
                "width": 150,
            },
            {
                "label": _("Customer Name"),
                "fieldname": "customer_name",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 240,
            },
            {
                "label": _("Status"),
                "fieldname": "status",
                "fieldtype": "Data",
                "width": 180,
            },
            {
                "label": _("VAT Status"),
                "fieldname": "vat_status",
                "fieldtype": "Data",
                "width": 180,
            },
            {
                "label": _("Sales"),
                "fieldname": "sales",
                "fieldtype": "Currency",
                "width": 150,
            },
            {
                "label": _("VAT"),
                "fieldname": "vat",
                "fieldtype": "Currency",
                "width": 150,
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
    start_date = filters.get('start_date')
    end_date = filters.get('end_date')
    valid_till = filters.get('valid_till')
    status = filters.get('status')
	
    quotation = frappe.qb.DocType("Quotation")
    quotation_item = frappe.qb.DocType("Quotation Item")
    sales_taxes_charges = frappe.qb.DocType("Sales Taxes and Charges")

    conditions = [quotation.docstatus < 2]
    
    if company:
        conditions.append(quotation.company == company)
    if start_date and end_date:
        conditions.append(quotation.transaction_date[start_date:end_date])
    if valid_till:
        conditions.append(quotation.valid_till == valid_till)
    if status == "Approved":
        conditions.append(quotation.workflow_state == "Approved")
    if status == "Pending Approval":
        conditions.append(quotation.workflow_state != "Approved")
        conditions.append(quotation.workflow_state != "Rejected")
        conditions.append(quotation.workflow_state != "Cancelled")


    query = frappe.qb.from_(quotation) \
        .inner_join(quotation_item) \
        .on(quotation_item.parent == quotation.name) \
        .inner_join(sales_taxes_charges) \
        .on(sales_taxes_charges.parent == quotation.name) \
        .select(
            quotation.transaction_date.as_("start_date"),
            quotation.valid_till.as_("valid_till"),
            quotation.name.as_("quotation_number"),
            quotation.customer_name,
            quotation.workflow_state.as_("status"),
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
        ).where(Criterion.all(conditions))

    data = query.run(as_dict=True)
    quotations = []
    report_data = []

    for row in data:
        row["indent"] = 1
        if row["quotation_number"] in quotations:
            report_data.append(row)
        else:
            quotations.append(row["quotation_number"])
            report_data.append({ "quotation_number": row["quotation_number"], "indent": 0, "bold": 1 })
            report_data.append(row)
            
    return report_data


