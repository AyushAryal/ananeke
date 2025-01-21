# ananeke/ananeke/create_workspace.py
import frappe

# def create_custom_workspace():
#     try:
#         # Define the workspace document
#         workspace = frappe.get_doc({
#             "doctype": "Workspace",
#             "title": "Frontdesk Workspace",  # Custom title for your workspace
#             "is_standard": 0,  # Set to 0 for custom workspaces
#             "module": "Ananeke",  # Your custom module name
#             "for_user": None,  # For all users with the specified role
#             "restrict_to_domain": None,
#             "public": 0,  # Set to 1 for public visibility
#             "hide_custom": 0,
#             "onboard": 0,
#             "extendable": 0,
#             "role": ["Frontdesk"],  # Role to restrict this workspace
#         })

#         # Insert the workspace into the database
#         workspace.insert(ignore_permissions=True)
#         frappe.db.commit()
#         frappe.msgprint(f"Workspace '{workspace.title}' created successfully!")
#     except Exception as e:
#         frappe.log_error(f"Error creating workspace: {str(e)}", "Workspace Creation Error")
#         frappe.msgprint(f"Error: {str(e)}")

# Run the function to create the workspace
# create_custom_workspace()
