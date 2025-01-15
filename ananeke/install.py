import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def add_custom_field(doc, after_field, field_details, section=None):
    if section:
        section_fieldname = f"{section.replace(' ', '_').lower()}_section"
        if not frappe.db.exists("Custom Field", {"dt": doc, "fieldname": section_fieldname}):
            section_definition = {
                "doctype": "Custom Field",
                "dt": doc,
                "fieldname": section_fieldname,
                "fieldtype": "Section Break",
                "label": section,
                "insert_after": after_field
            }
            create_custom_field(doc, section_definition)
            frappe.db.commit()
            print(f"Section '{section}' added successfully.")

        after_field = section_fieldname

    field_definition = {
        "doctype": "Custom Field",
        "dt": doc,
        "fieldname": field_details.get("field_name"),
        "fieldtype": field_details.get("field_type"),
        "label": field_details.get("label"),
        "hidden": field_details.get("hidden", 0),
        "options": field_details.get("options"),
        "reqd": field_details.get("reqd", 0),
        "insert_after": after_field,
    }

    if not frappe.db.exists("Custom Field", {"dt": doc, "fieldname": field_details.get("field_name")}):
        create_custom_field(doc, field_definition)
        frappe.db.commit()
        print(f"Custom field '{field_details.get('field_name')}' added successfully.")
    else:
        print(f"Custom field '{field_details.get('field_name')}' already exists.")



def field_generator():
    yield {
        "doc": "Sales Order",
        "after_field": "transaction_date",
        "field_details": {
            "field_name": "service_date_time",
            "field_type": "Datetime",
            "label": "Service Datetime "
        }
    }
    yield {
        "doc": "Todo",
        "after_field": "date",
        "field_details": {
            "field_name": "start_date_time",
            "field_type": "Datetime",
            "label": "Start Datetime "
        }
    }
    yield {
        "doc": "Todo",
        "after_field": "start_date_time",
        "field_details": {
            "field_name": "end_date_time",
            "field_type": "Datetime",
            "label": "End Datetime "
        }
    }
    

def before_install():
    ...
    


def after_install():
    for field in field_generator():
        add_custom_field(
            doc=field["doc"],
            after_field=field["after_field"],
            field_details=field["field_details"],
            section=field.get("section")
        )