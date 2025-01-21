import frappe
from frappe.model.mapper import get_mapped_doc


def sales_order(doc, method):
    if method == "before_save":
        # if doc.service_date_time:
        #     doc.delivery_date = doc.service_date_time.split(" ")[0]
        ...


@frappe.whitelist()
def make_appointment(source_name, target_doc=None):
    doc = get_mapped_doc(
        "Customer",
        source_name,
        {
            "Customer": {
                "doctype": "Sales Order",
                "field_map": [
                    ["patient", "name"],
                    ["company", "company"],
                ],
            }
        },
        target_doc,
    )
    return doc