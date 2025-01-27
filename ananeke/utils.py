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


def update_field_property(doctype, fieldname, property_name, value):
    if not frappe.db.exists(
        "Property Setter",
        {"doc_type": doctype, "field_name": fieldname, "property": property_name},
    ):
        frappe.get_doc({
            "doctype": "Property Setter",
            "doc_type": doctype,
            "doctype_or_field": "DocField",
            "field_name": fieldname,
            "property": property_name,
            "value": value,
            "property_type": "Check" if isinstance(value, int) else "Data",
        }).insert()
        frappe.db.commit()
        print(f"Property '{property_name}' for field '{fieldname}' in Doctype '{doctype}' updated to {value}.")
    else:
        print(f"Property Setter for '{property_name}' on '{fieldname}' in Doctype '{doctype}' already exists.")
