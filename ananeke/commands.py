import click
import frappe
from frappe import _

def delete_workspace_with_sql():
    workspace_name = "Frontdesk"

    exists = frappe.db.sql("""
        SELECT name 
        FROM `tabWorkspace` 
        WHERE name = %s
    """, (workspace_name,))

    if exists:
        frappe.db.sql("""
            DELETE FROM `tabWorkspace` 
            WHERE name = %s
        """, (workspace_name,))

        frappe.db.commit()

        print(f"Workspace '{workspace_name}' deleted successfully.")
        return
    print(f"Workspace {workspace_name} does not exist")
    


def create_workspace_with_sql():
    workspace_name = "Frontdesk"
    title = "FrontDesk"
    module = "Ananeke"
    label = "Front Desk Workspace",
    public = 1,
    content = "{}"
    icon = "fa fa-folder"

    columns = frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace`", as_dict=True)
    column_names = [col["Field"] for col in columns]
    print("Columns in `tabWorkspace` table:", ", ".join(column_names))

    exists = frappe.db.sql("""
        SELECT name 
        FROM `tabWorkspace` 
        WHERE name = %s
    """, (workspace_name,))
    
    if exists:
        print(f"Workspace '{workspace_name}' already exists.")
        return

    frappe.db.sql("""
        INSERT INTO `tabWorkspace` 
        (`name`,`roles`,`public`, `title`,`module`, `label`, `content`, `creation`, `modified`, `modified_by`, `owner`, `idx`, `icon`)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s)
    """, (
        workspace_name,  # Unique name for the workspace
        public,
        title,
        module,          # Module the workspace belongs to
        label,           # Label displayed for the workspace
        content,         # JSON content for workspace details
        "Administrator", # User who last modified it
        "Administrator", # Owner of the workspace
        0,               # Index position (used for ordering)
        icon             # Icon for the workspace
    ))

    frappe.db.commit()

    print(f"Workspace '{workspace_name}' created successfully.")


@click.command('create-workspace')
@click.argument('workspace_name')
@click.argument('workspace_type')
@click.option('--owner', default=None, help="Owner of the workspace")
@click.option('--description', default=None, help="Description for the workspace")
def create_workspace_command(workspace_name, workspace_type, owner, description):
    try:
        frappe.init(site="site.wallet")
        frappe.connect()
        delete_workspace_with_sql()

        create_workspace_with_sql()
        workspaces = frappe.db.sql("SELECT * FROM `tabWorkspace`", as_dict=True)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()

commands = [
    create_workspace_command
]
