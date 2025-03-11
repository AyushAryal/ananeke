import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
        {"label": "Assigned To", "fieldname": "assign_to", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Item", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Quantity", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Sales Invoice", "fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": "Invoice Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
    ]

    conditions = []
    values = {}

    if filters.get("assign_to"):
        conditions.append("si_item.assign_to = %(assign_to)s")
        values["assign_to"] = filters["assign_to"]

    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        values["from_date"] = filters["from_date"]

    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        values["to_date"] = filters["to_date"]

    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")
        values["customer"] = filters["customer"]

    if filters.get("status"):
        conditions.append("si.status = %(status)s")
        values["status"] = filters["status"]

    if filters.get("company"):
        conditions.append("si.company = %(company)s")
        values["company"] = filters["company"]

    conditions_sql = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT 
            si_item.assign_to, emp.employee_name, si.name AS sales_invoice, 
            si.customer, si_item.item_name, si_item.qty, 
            si_item.amount, si.posting_date, si.company, si.status
        FROM `tabSales Invoice Item` si_item
        JOIN `tabSales Invoice` si ON si.name = si_item.parent
        LEFT JOIN `tabEmployee` emp ON emp.name = si_item.assign_to
        WHERE {conditions_sql}
        ORDER BY si.posting_date DESC, si_item.assign_to ASC
    """

    data = frappe.db.sql(query, values, as_dict=True)
    
    total_amount = sum(row["amount"] for row in data if row["amount"])
    total_qty = sum(row["qty"] for row in data if row["qty"])
    
    
    total_row = {
        "assign_to": "",
        "employee_name": "",
        "customer": "",
        "item_name": "Total",
        "qty": total_qty,
        "amount": total_amount,
        "status": "",
    }
    data.append(total_row)

    return columns, data


