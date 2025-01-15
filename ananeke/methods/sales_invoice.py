import json
import frappe

@frappe.whitelist()
def get_customer_numbers(invoices):
    if isinstance(invoices, str):
        try:
            invoices = json.loads(invoices)
        except json.JSONDecodeError:
            frappe.throw("Invalid JSON format for invoices.")

    if not isinstance(invoices, list):
        frappe.throw("Invalid data format. Expected a list of invoices.")

    customer_numbers = []

    for invoice in invoices:
        try:
            sales_invoice = frappe.get_doc("Sales Invoice", invoice)
            contact = frappe.get_doc("Contact", sales_invoice.contact_person)
            customer_numbers.append(contact.mobile_no)

        except Exception as e:
            frappe.log_error(f"Error processing invoice {invoice}: {str(e)}", "Customer Contact Fetch Error")

    return {"contacts":customer_numbers}
