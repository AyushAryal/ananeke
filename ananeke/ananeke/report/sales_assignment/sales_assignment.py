import frappe
from frappe import _

def execute(filters=None):
    filters = filters or {}

    columns = [
        # {"label": "Sales Person", "fieldname": "assign_to", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
        {"label": "Item", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
        {"label": "Nature", "fieldname": "item_group", "fieldtype": "Data", "width": 200},
        # {"label": "Quantity", "fieldname": "qty", "fieldtype": "Float", "width": 100},
        {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
        {"label": "Sales Invoice", "fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
        {"label": "Invoice Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        # {"label": "Commission", "fieldname": "commission_value", "fieldtype": "Percent", "width": 100}
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
        conditions.append("si.status IN %(status)s")
        values["status"] = filters["status"]

    if filters.get("company"):
        conditions.append("si.company = %(company)s")
        values["company"] = filters["company"]

    conditions_sql = " AND ".join(conditions) if conditions else "1=1"

    query = f"""
        SELECT 
            si_item.assign_to, emp.employee_name, si.name AS sales_invoice, 
            si.customer, si_item.item_name, si_item.item_group, si_item.qty, 
            si_item.amount, si.posting_date, si.company, si.status, 
            item.commission_value  -- Get commission_value from the Item table
        FROM `tabSales Invoice Item` si_item
        JOIN `tabSales Invoice` si ON si.name = si_item.parent
        LEFT JOIN `tabEmployee` emp ON emp.name = si_item.assign_to
        LEFT JOIN `tabItem` item ON item.name = si_item.item_code  -- Join with the Item table to get commission_value
        WHERE {conditions_sql}
        ORDER BY si.posting_date DESC, si_item.assign_to ASC
    """

    data = frappe.db.sql(query, values, as_dict=True)

    employee_sales = {}
    for row in data:
        if row["assign_to"] not in employee_sales:
            employee_sales[row["assign_to"]] = {"employee_name": row["employee_name"], "total_amount": 0, "total_commission": 0}
        
        employee_sales[row["assign_to"]]["total_amount"] += row["amount"]
        employee_sales[row["assign_to"]]["total_commission"] += row["commission_value"]

    sorted_employees = sorted(employee_sales.items(), key=lambda x: x[1]["total_amount"], reverse=True)

    total_amount = sum(row["amount"] for row in data if row["amount"])
    total_qty = sum(row["qty"] for row in data if row["qty"])
    total_commission = sum(row["commission_value"] for row in data if row["commission_value"])

    total_row = {
        "assign_to": "",
        "employee_name": "",
        "customer": "",
        "item_name": "Total",
        "qty": total_qty,
        "amount": total_amount,
        "commission_value": total_commission,  # Add total commission to the total row
        "status": "",
    }

    data.append(total_row)

    return columns, data


# import frappe
# from frappe import _

# def execute(filters=None):
#     filters = filters or {}

#     columns = [
#         {"label": "Sales Person", "fieldname": "assign_to", "fieldtype": "Link", "options": "Employee", "width": 150},
#         {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 150},
#         {"label": "Item", "fieldname": "item_name", "fieldtype": "Data", "width": 200},
#         {"label": "Quantity", "fieldname": "qty", "fieldtype": "Float", "width": 100},
#         {"label": "Amount", "fieldname": "amount", "fieldtype": "Currency", "width": 120},
#         {"label": "Sales Invoice", "fieldname": "sales_invoice", "fieldtype": "Link", "options": "Sales Invoice", "width": 150},
#         {"label": "Invoice Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
#         {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
#         {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
#     ]

#     conditions = []
#     values = {}

#     if filters.get("assign_to"):
#         conditions.append("si_item.assign_to = %(assign_to)s")
#         values["assign_to"] = filters["assign_to"]

#     if filters.get("from_date"):
#         conditions.append("si.posting_date >= %(from_date)s")
#         values["from_date"] = filters["from_date"]

#     if filters.get("to_date"):
#         conditions.append("si.posting_date <= %(to_date)s")
#         values["to_date"] = filters["to_date"]

#     if filters.get("customer"):
#         conditions.append("si.customer = %(customer)s")
#         values["customer"] = filters["customer"]

#     if filters.get("status"):
#         conditions.append("si.status IN %(status)s")
#         values["status"] = filters["status"]

#     if filters.get("company"):
#         conditions.append("si.company = %(company)s")
#         values["company"] = filters["company"]

#     conditions_sql = " AND ".join(conditions) if conditions else "1=1"

#     query = f"""
#         SELECT 
#             si_item.assign_to, emp.employee_name, si.name AS sales_invoice, 
#             si.customer, si_item.item_name, si_item.qty, 
#             si_item.amount, si.posting_date, si.company, si.status
#         FROM `tabSales Invoice Item` si_item
#         JOIN `tabSales Invoice` si ON si.name = si_item.parent
#         LEFT JOIN `tabEmployee` emp ON emp.name = si_item.assign_to
#         WHERE {conditions_sql}
#         ORDER BY si.posting_date DESC, si_item.assign_to ASC
#     """

#     data = frappe.db.sql(query, values, as_dict=True)

#     # Group the data by `assign_to` (Sales Person)
#     grouped_data = {}
#     for row in data:
#         if row["assign_to"] not in grouped_data:
#             grouped_data[row["assign_to"]] = {"employee_name": row["employee_name"], "rows": [], "total_amount": 0, "total_qty": 0}
        
#         grouped_data[row["assign_to"]]["rows"].append(row)
#         grouped_data[row["assign_to"]]["total_amount"] += row["amount"]
#         grouped_data[row["assign_to"]]["total_qty"] += row["qty"]

#     # Now format the data: create a summary row, and add gaps between groups
#     formatted_data = []
#     for assign_to, group in grouped_data.items():
#         # Add a bold summary row for each `assign_to` (Sales Person)
#         summary_row = {
#             "assign_to": assign_to,
#             "employee_name": group["employee_name"],
#             "item_name": "Summary",  # Indicate summary row
#             "qty": group["total_qty"],  # Total quantity for the group
#             "amount": group["total_amount"],  # Total amount for the group
#             "sales_invoice": "",
#             "posting_date": "",
#             "customer": "",
#             "status": "",
#         }

#         # Add the summary row
#         formatted_data.append(summary_row)

#         # Add the actual rows for this `assign_to` with indentation logic
#         for row in group["rows"]:
#             indented_row = row.copy()
#             indented_row["item_name"] = f"  {row['item_name']}"  # Add 2 spaces to indent each item row
#             formatted_data.append(indented_row)

#         # Add an empty row (gap) after each group
#         formatted_data.append({})  # Empty row for gap

#     # Add the overall total row (can also be added at the end of the formatted data)
#     total_amount = sum(row["amount"] for row in data if row["amount"])
#     total_qty = sum(row["qty"] for row in data if row["qty"])

#     total_row = {
#         "assign_to": "",
#         "employee_name": "",
#         "customer": "",
#         "item_name": "Total",
#         "qty": total_qty,
#         "amount": total_amount,
#         "status": "",
#     }

#     formatted_data.append(total_row)

#     return columns, formatted_data
