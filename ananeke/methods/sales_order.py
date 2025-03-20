import frappe
from frappe.model.mapper import get_mapped_doc


def sales_order(doc, method):
    if method == "on_submit":
        for item in doc.items:
            try:
                if item.assign_to:
                    employee = frappe.get_doc("Employee", item.assign_to)
                    customer = frappe.get_doc("Customer", doc.customer, fields=["name", "customer_name", "mobile_n0"])

                    try:
                        task = frappe.get_doc({
                            "doctype": "ToDo",
                            "description": f"{item.item_name} appointment with {customer.customer_name} at {doc.service_date_time} : ({doc.name})",
                            "status": "Open",
                            "allocated_to": employee.user_id,
                            "assigned_to": employee.user_id,
                            "assigned_by": frappe.session.user,
                            "reference_type": "Sales Order",
                            "reference_name": doc.name,
                        })
                        task.save() 
                        if task.name:
                            notification_message = f"Task assigned:{item.item_name} by {frappe.session.user}."

                            try:
                                notification = frappe.get_doc({
                                    "doctype": "Notification Log",
                                    "for_user": employee.user_id,
                                    "subject": notification_message,
                                    "link": f"/app/todo/{task.name}",
                                    "type": "Assignment"  
                                })
                                notification.insert(ignore_permissions=True)
                                frappe.msgprint(f"In-app notification sent to {employee.user_id}")
                            except Exception as notification_error:
                                frappe.log_error(f"Error sending notification: {str(notification_error)}", "Notification Error")
                    except Exception as task_error:
                        frappe.log_error(f"Error creating task: {str(task_error)}", "Task Creation Error")
                        frappe.msgprint(f"Failed to create the task for {employee.user_id}.")


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