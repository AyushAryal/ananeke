import frappe
from .utils import add_custom_field, update_field_property


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


