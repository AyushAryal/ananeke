import frappe

def stock_entry(doc,method):
    if method == "before_save":
        if doc.stock_entry_type == "Material Consumption for Manufacture" and not doc.from_warehouse:
            frappe.throw("Source Warehouse is compulsory for Stock Entry Type: Material Consumption for Manufacture")