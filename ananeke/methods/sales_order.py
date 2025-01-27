import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import nowdate
from frappe.push_notification import PushNotification


def sales_order(doc, method):
    if method == "on_submit":
        for item in doc.items:
            try:
                if item.assign_to:
                    employee = frappe.get_doc("Employee", item.assign_to)
                    user = frappe.get_doc(doctype="User", email=employee.user_id)

                    task = frappe.get_doc({
                        "doctype": "ToDo",
                        "description": f"Task assigned for {item.item_name} for appointment {doc.name} with {doc.customer}",
                        "status": "Open",
                        "allocated_to": employee.user_id,
                        "assign_to": employee.user_id,
                        "reference_type": "Sales Order",
                        "reference_name": doc.name,
                    })
                    task.save()

                    notification_message = f"You have been assigned a task for Sales Order {doc.name}."
                    
                    frappe.publish_realtime(
                        event="notification",
                        message={
                            "event": "Notification",
                            "message": notification_message,
                            "user": employee.user_id,
                            "task_url": f"/app/todo/{task.name}" 
                        },
                        user=employee.user_id
                    )

                    frappe.msgprint(f"Task created and real-time notification sent to {employee.employee_name} for item {item.item_name}.")
            except Exception as e:
                frappe.log_error(f"Error while creating task and notification for Sales Order {doc.name}, Item: {item.item_name}. Error: {str(e)}")
                frappe.msgprint(f"An error occurred while assigning task to {item.item_name}. Please check the logs.")


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