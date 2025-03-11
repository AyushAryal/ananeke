import json
import frappe


def sales_invoice(doc, method):
    selling_settings = frappe.get_single("Selling Settings")
    commission_expense_account = selling_settings.commission_expense_account
    commission_payable_account = selling_settings.commission_payable_account

    if method == "on_submit":
        total_commission = 0
        employee_commissions = {}

        if commission_expense_account:
            for item in doc.items:
                item_doc = frappe.get_doc("Item", item.item_code)
                commission_value = item_doc.get("commission_value") or 0
                commission_amount = (commission_value / 100) * (item.qty * item.rate)

                employee = item.get("assign_to")

                if employee:
                    if employee not in employee_commissions:
                        employee_commissions[employee] = 0
                    employee_commissions[employee] += commission_amount
                else:
                    frappe.log_error(
                        title="Commission Calculation",
                        message=f"Item: {item.item_code}, Amount: {item.amount}, Commission (%): {commission_value}, Commission Amount: {commission_amount}, No employee assigned",
                    )

                item.net_amount = item.amount - commission_amount

                frappe.log_error(
                    title="Commission Calculation",
                    message=f"Item: {item.item_code}, Amount: {item.amount}, Commission (%): {commission_value}, Commission Amount: {commission_amount}, Employee: {employee or 'Not Assigned'}",
                )

                if employee:
                    total_commission += commission_amount

            if total_commission == 0:
                return

            create_commission_journal_entry(doc, total_commission, commission_expense_account, commission_payable_account, employee_commissions)

    elif method == "on_cancel":
        reverse_commission_journal_entry(doc, commission_expense_account, commission_payable_account)
    

def create_commission_journal_entry(doc, total_commission, commission_expense_account, commission_payable_account, employee_commissions):
    accounts = [
        {
            "account": commission_expense_account,
            "debit_in_account_currency": total_commission,
            "credit_in_account_currency": 0,
        }
    ]

    total_payable = 0

    for employee, commission_amount in employee_commissions.items():
        accounts.append(
            {
                "account": commission_payable_account,
                "debit_in_account_currency": 0,
                "credit_in_account_currency": commission_amount,
                "party_type": "Employee",
                "party": employee,
            }
        )
        total_payable += commission_amount

    if total_commission != total_payable:
        frappe.throw(f"Total Debit must be equal to Total Credit. Difference: {total_commission - total_payable}")

    journal_entry = frappe.get_doc(
        {
            "doctype": "Journal Entry",
            "voucher_type": "Journal Entry",
            "posting_date": doc.posting_date,
            "accounts": accounts,
            "remarks": f"Commission for Sales Invoice {doc.name}",
            "user_remark": f"Commission for Sales Invoice {doc.name}"
        }
    )

    journal_entry.insert()
    journal_entry.submit()

    doc.db_set("commission_journal_entry", journal_entry.name)


def reverse_commission_journal_entry(doc, commission_account, commission_payable_account):
    if not doc.commission_journal_entry:
        return

    original_journal_entry = frappe.get_doc("Journal Entry", doc.commission_journal_entry)

    reversed_accounts = []

    for account in original_journal_entry.accounts:
        reversed_accounts.append({
            "account": account.account,
            "debit_in_account_currency": account.credit_in_account_currency,
            "credit_in_account_currency": account.debit_in_account_currency,
            "party_type": account.party_type if account.party_type else None,
            "party": account.party if account.party else None,
        })

    reversal_entry = frappe.get_doc({
        "doctype": "Journal Entry",
        "voucher_type": "Journal Entry",
        "posting_date": frappe.utils.today(),
        "accounts": reversed_accounts,
        "remarks": f"Reversal of Commission for Canceled Sales Invoice {doc.name}",
        "user_remark": f"Reversal of Commission for Canceled Sales Invoice {doc.name}"
    })

    reversal_entry.insert()
    reversal_entry.submit()

    doc.db_set("commission_journal_entry", None)



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
            frappe.log_error(
                f"Error processing invoice {invoice}: {str(e)}",
                "Customer Contact Fetch Error",
            )

    return {"contacts": customer_numbers}
