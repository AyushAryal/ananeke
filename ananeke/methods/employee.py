import frappe
from erpnext.accounts.utils import get_balance_on

@frappe.whitelist()
def employee_accumulated_commission(employee_id):
    selling_settings = frappe.get_single("Selling Settings")

    employee = frappe.get_doc(doctype="Employee", name=employee_id)

    commission_payable_account = selling_settings.commission_payable_account

    if not commission_payable_account:
        return {"message": "Commission Payable account not configured."}
    
    balance = get_balance_on(
        account=commission_payable_account,
        party_type="Employee",
        party=employee.name,
    )

    return {
        "employee_id": employee_id,
        "employee_name": employee.employee_name,
        "accumulated_commission": -balance
    }
