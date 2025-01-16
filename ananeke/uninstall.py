import frappe


def remove_custom_field(doc, fieldname):
    if frappe.db.exists("Custom Field", {"dt": doc, "fieldname": fieldname}):
        custom_field = frappe.get_doc("Custom Field", {"dt": doc, "fieldname": fieldname})
        custom_field.delete()
        frappe.db.commit()
        print(f"Custom field '{fieldname}' removed successfully from DocType '{doc}'.")
    else:
        print(f"Custom field '{fieldname}' does not exist in DocType '{doc}'.")


def remove_property_setter(doc, fieldname, property_name):
    if frappe.db.exists(
        "Property Setter",
        {"doc_type": doc, "field_name": fieldname, "property": property_name},
    ):
        property_setter = frappe.get_doc(
            "Property Setter",
            {"doc_type": doc, "field_name": fieldname, "property": property_name},
        )
        property_setter.delete()
        frappe.db.commit()
        print(f"Property Setter '{property_name}' for field '{fieldname}' in DocType '{doc}' removed.")
    else:
        print(f"Property Setter '{property_name}' for field '{fieldname}' in DocType '{doc}' does not exist.")


def field_generator_for_uninstall():
    return [
        {
            "doc": "Sales Order",
            "fields": ["service_date_time"],
            "property_setters": [
                {"fieldname": "delivery_date", "property_name": "in_list_view"},
                {"fieldname": "cost_center", "property_name": "in_list_filter"},
            ],
        },
        {
            "doc": "Todo",
            "fields": ["start_date_time", "end_date_time"],
            "property_setters": [],
        },
    ]


def before_uninstall():
    for entry in field_generator_for_uninstall():
        doc = entry["doc"]

        for fieldname in entry["fields"]:
            try:
                remove_custom_field(doc, fieldname)
            except Exception as e:
                print(f"Error removing custom field '{fieldname}' from DocType '{doc}': {e}")

        for setter in entry["property_setters"]:
            try:
                remove_property_setter(
                    doc=doc,
                    fieldname=setter["fieldname"],
                    property_name=setter["property_name"],
                )
            except Exception as e:
                print(f"Error removing property setter for field '{setter['fieldname']}' in DocType '{doc}': {e}")
