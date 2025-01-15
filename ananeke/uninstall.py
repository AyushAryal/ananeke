import frappe

def remove_custom_field(doc, field_name):
    if frappe.db.exists("Custom Field", {"dt": doc, "fieldname": field_name}):
        frappe.db.delete("Custom Field", {"dt": doc, "fieldname": field_name})
        frappe.db.commit()

# ----------------------------------------------------------------------------------------------

def before_uninstall():
    remove_custom_field(
        doc="Sales Order",
        field_name="service_date_time"
    )

    remove_custom_field(
        doc="Todo",
        field_name="start_date_time"
    )

    remove_custom_field(
        doc="Todo",
        field_name="end_date_time"
    )