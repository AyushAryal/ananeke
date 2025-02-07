import json
import frappe


def sales_invoice(doc,method):
    if method == "before_save":
        service_commission_account = "Commission on service -A"
        total_commission = 0

        for item in doc.items:
            item_doc = frappe.get_doc("Item", item.item_code)
            commission_value = item_doc.get("commission_value") or 0
            commission_amount = commission_value
            total_commission += commission_amount
            item.net_amount = item.amount - commission_amount

            frappe.log_error(
                title="Commission Calculation",
                message=f"Item: {item.item_code}, Amount: {item.amount}, Commission (%): {commission_value}, Commission Amount: {commission_amount}"
            )

        # frappe.throw(f"Total Commission: {total_commission}")

        if total_commission == 0:
            return

        create_commission_journal_entry(doc, total_commission, service_commission_account)

    if method == "on_submit":
        ...

def create_commission_journal_entry(doc, total_commission, service_commission_account):
    journal_entry = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Journal Entry",
        "posting_date": doc.posting_date,
        "accounts": [
            {
                "account": service_commission_account,
                "debit_in_account_currency": total_commission,
                "credit_in_account_currency": 0,
            },
            {
                "account": doc.debit_to,
                "debit_in_account_currency": 0,
                "credit_in_account_currency": total_commission,
            }
        ],
        "remarks": f"Commission for Sales Invoice {doc.name}"
    })

    journal_entry.insert()
    journal_entry.submit()

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
