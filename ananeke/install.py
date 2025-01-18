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
            "label": "Service Datetime"
        }
    }
    yield {
        "doc": "Todo",
        "after_field": "date",
        "field_details": {
            "field_name": "start_date_time",
            "field_type": "Datetime",
            "label": "Start Datetime"
        }
    }
    yield {
        "doc": "Todo",
        "after_field": "start_date_time",
        "field_details": {
            "field_name": "end_date_time",
            "field_type": "Datetime",
            "label": "End Datetime"
        }
    }


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


def after_install():
    for field in field_generator():
        try:
            add_custom_field(
                doc=field["doc"],
                after_field=field["after_field"],
                field_details=field["field_details"],
                section=field.get("section"),
            )
        except Exception as e:
            print(f"Error adding field '{field['field_details']['field_name']}': {e}")

    try:
        update_field_property(
            doctype="Sales Order",
            fieldname="delivery_date",
            property_name="in_list_view",
            value=0,
        )
    except Exception as e:
        print(f"Error updating 'delivery_date' in 'Sales Order': {e}")

    try:
        update_field_property(
            doctype="Sales Order",
            fieldname="cost_center",
            property_name="in_list_filter",
            value=1,
        )
    except Exception as e:
        print(f"Error updating 'cost_center' in 'Sales Order': {e}")

    try:
        update_field_property(
            doctype="ToDo",
            fieldname="date",
            property_name="in_list_view",
            value=0,
        )
    except Exception as e:
        print(f"Error updating 'date' in 'ToDo': {e}")

    try:
        update_field_property(
            doctype="Item",
            fieldname="standard_rate",
            property_name="in_list_view",
            value=1,
        )
    except Exception as e:
        print(f"Error updating 'standard_rate' in 'Item': {e}")

