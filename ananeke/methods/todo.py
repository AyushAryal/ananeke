import frappe


def todo(doc,method):
    if method == "before_save":
        if doc.reference_type == "Sales Order":
            sales_order = frappe.get_doc("Sales Order", doc.reference_name)
            doc.start_date_time = sales_order.service_date_time if (sales_order.service_date_time and not doc.start_date_time ) else doc.start_date_time
