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
    content = '[{"id":"Cj2TyhgiWy","type":"chart","data":{"chart_name":"Territory Wise Sales","col":12}},{"id":"LAKRmpYMRA","type":"spacer","data":{"col":12}},{"id":"XGIwEUStw_","type":"header","data":{"text":"<span class=\"h4\"><b>Your Shortcuts</b></span>","col":12}},{"id":"69RN0XsiJK","type":"shortcut","data":{"shortcut_name":"Lead","col":3}},{"id":"t6PQ0vY-Iw","type":"shortcut","data":{"shortcut_name":"Opportunity","col":3}},{"id":"VOFE0hqXRD","type":"shortcut","data":{"shortcut_name":"Customer","col":3}},{"id":"0ik53fuemG","type":"shortcut","data":{"shortcut_name":"Sales Analytics","col":3}},{"id":"wdROEmB_XG","type":"shortcut","data":{"shortcut_name":"Dashboard","col":3}},{"id":"-I9HhcgUKE","type":"spacer","data":{"col":12}},{"id":"ttpROKW9vk","type":"header","data":{"text":"<span class=\"h4\"><b>Reports &amp; Masters</b></span>","col":12}},{"id":"-76QPdbBHy","type":"card","data":{"card_name":"Sales Pipeline","col":4}},{"id":"_YmGwzVWRr","type":"card","data":{"card_name":"Masters","col":4}},{"id":"Bma1PxoXk3","type":"card","data":{"card_name":"Reports","col":4}},{"id":"80viA0R83a","type":"card","data":{"card_name":"Campaign","col":4}},{"id":"Buo5HtKRFN","type":"card","data":{"card_name":"Settings","col":4}},{"id":"sLS_x4FMK2","type":"card","data":{"card_name":"Maintenance","col":4}}]'
    icon = "getting-started"

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
        (`name`,`public`, `title`,`module`, `label`, `content`, `creation`, `modified`, `modified_by`, `owner`, `idx`, `icon`)
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
def create_workspace_command():
    try:
        frappe.init(site="site.wallet")
        frappe.connect()
        delete_workspace_with_sql()

        create_workspace_with_sql()
        workspaces = frappe.db.sql("SELECT * FROM `tabWorkspace`", as_dict=True)
        for workspace in workspaces:
            if workspace.name == 'Frontdesk' or workspace.name == 'CRM':
                print(f"{workspace.name}:{workspace.content}\n\n")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()

commands = [
    create_workspace_command
]
