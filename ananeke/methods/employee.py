import frappe
from erpnext.accounts.utils import get_balance_on
from frappe.utils import today, getdate


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



@frappe.whitelist()
def check_employee_checked_in_today():
    sql_query = """
        SELECT e.name
        FROM `tabEmployee` e
        JOIN `tabEmployee Checkin` ec ON e.name = ec.employee
        WHERE ec.log_type = 'IN'
          AND DATE(ec.time) = CURDATE()
        ORDER BY ec.time DESC
    """

    checked_in_employees = frappe.db.sql(sql_query, as_list=True)

    employee_names = [emp[0] for emp in checked_in_employees]

    return checked_in_employees

