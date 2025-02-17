import click
import frappe
from frappe import _
from .utils import add_custom_field
from frappe.custom.doctype.custom_field.custom_field import create_custom_field


def delete_workspace_with_sql():
    workspace_name = "Frontdesk"
    exists = frappe.db.sql(
        """
        SELECT name 
        FROM `tabWorkspace` 
        WHERE name = %s
    """,
        (workspace_name,),
    )

    if exists:
        frappe.db.sql(
            """
            DELETE FROM `tabWorkspace` 
            WHERE name = %s
        """,
            (workspace_name,),
        )

        frappe.db.commit()

        print(f"Workspace '{workspace_name}' deleted successfully.")
        return
    print(f"Workspace {workspace_name} does not exist")


def create_workspace_with_sql():
    workspace_name = "Frontdesk"
    title = "FrontDesk"
    module = "Ananeke"
    label = ("Front Desk Workspace",)
    public = (1,)
    content = '[{"id":"Cj2TyhgiWy","type":"chart","data":{"chart_name":"Territory Wise Sales","col":12}},{"id":"LAKRmpYMRA","type":"spacer","data":{"col":12}},{"id":"XGIwEUStw_","type":"header","data":{"text":"<span class="h4"><b>Your Shortcuts</b></span>","col":12}},{"id":"69RN0XsiJK","type":"shortcut","data":{"shortcut_name":"Lead","col":3}},{"id":"t6PQ0vY-Iw","type":"shortcut","data":{"shortcut_name":"Opportunity","col":3}},{"id":"VOFE0hqXRD","type":"shortcut","data":{"shortcut_name":"Customer","col":3}},{"id":"0ik53fuemG","type":"shortcut","data":{"shortcut_name":"Sales Analytics","col":3}},{"id":"wdROEmB_XG","type":"shortcut","data":{"shortcut_name":"Dashboard","col":3}},{"id":"-I9HhcgUKE","type":"spacer","data":{"col":12}},{"id":"ttpROKW9vk","type":"header","data":{"text":"<span class="h4"><b>Reports &amp; Masters</b></span>","col":12}},{"id":"-76QPdbBHy","type":"card","data":{"card_name":"Sales Pipeline","col":4}},{"id":"_YmGwzVWRr","type":"card","data":{"card_name":"Masters","col":4}},{"id":"Bma1PxoXk3","type":"card","data":{"card_name":"Reports","col":4}},{"id":"80viA0R83a","type":"card","data":{"card_name":"Campaign","col":4}},{"id":"Buo5HtKRFN","type":"card","data":{"card_name":"Settings","col":4}},{"id":"sLS_x4FMK2","type":"card","data":{"card_name":"Maintenance","col":4}}]'
    icon = "getting-started"

    columns = frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace`", as_dict=True)
    column_names = [col["Field"] for col in columns]
    print("Columns in `tabWorkspace` table:", ", ".join(column_names))

    exists = frappe.db.sql(
        """
        SELECT name 
        FROM `tabWorkspace` 
        WHERE name = %s
    """,
        (workspace_name,),
    )

    if exists:
        print(f"Workspace '{workspace_name}' already exists.")
        return

    frappe.db.sql(
        """
        INSERT INTO `tabWorkspace` 
        (`name`,`public`, `title`,`module`, `label`, `content`, `creation`, `modified`, `modified_by`, `owner`, `idx`, `icon`)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW(), %s, %s, %s, %s)
    """,
        (
            workspace_name,  # Unique name for the workspace
            public,
            title,
            module,  # Module the workspace belongs to
            label,  # Label displayed for the workspace
            content,  # JSON content for workspace details
            "Administrator",  # User who last modified it
            "Administrator",  # Owner of the workspace
            0,  # Index position (used for ordering)
            icon,  # Icon for the workspace
        ),
    )

    frappe.db.commit()
    print(f"Workspace '{workspace_name}' created successfully.")


@click.command("create-workspace")
def create_workspace_command():
    try:
        frappe.init(site="site.local")
        frappe.connect()
        delete_workspace_with_sql()

        create_workspace_with_sql()
        workspaces = frappe.db.sql("SELECT * FROM `tabWorkspace`", as_dict=True)
        for workspace in workspaces:
            if workspace.name == "Frontdesk" or workspace.name == "CRM":
                print(f"{workspace.name}:{workspace.content}\n\n")

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()


# -----------------------------------------------------------------------------------------------------------------


@click.command("create-assign-to-column")
def create_column():
    try:
        frappe.init(site="site.local")
        frappe.connect()
        field_definition = {
            "fieldname": "assign_to",
            "label": "Assign To",
            "fieldtype": "Link",
            "options": "Employee",
            "insert_after": "description",
            "read_only": 0,
            "in_list_view": 1,
            "mandatory": 0,
        }
        create_custom_field("Sales Order Item", field_definition)
        create_custom_field("Sales Invoice Item", field_definition)

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()


# @click.command('create-next-service-column')
# def create_column():
#     try:
#         frappe.init(site="site.local")
#         frappe.connect()
#         field_definition = {
#         "fieldname": "next_service",
#         "label": "Next Service",
#         "fieldtype": "Date",
#         "insert_after": "description",
#         "read_only": 0,
#         "in_list_view": 1,
#         "mandatory": 0,
#     }
#         create_custom_field("Sales Order Item", field_definition)
#         create_custom_field("Sales Invoice Item", field_definition)

#     except Exception as e:
#         click.echo(f"Error: {str(e)}")
#     finally:
#         frappe.destroy()


@click.command("add-commission-on-item")
def add_commission_on_item():
    try:
        frappe.init(site="site.local")
        frappe.connect()
        field = {
            "doc": "Item",
            "after_field": "has_variants",
            "field_details": {
                "field_name": "commission_value",
                "field_type": "Percent",
                "label": "Commision Value",
            },
        }

        add_custom_field(
            doc=field["doc"],
            after_field=field["after_field"],
            field_details=field["field_details"],
            section=field.get("section"),
        )

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()


@click.command("add-cost-center-to-user")
def add_cost_center_to_user():
    try:
        frappe.init(site="site.local")
        frappe.connect()
        field = {
            "doc": "User",
            "after_field": "email",
            "field_details": {
                "field_name": "cost_center",
                "field_type": "Link",
                "options": "Cost Center",
                "reqd": 0,
                "label": "Branch",
            },
        }

        add_custom_field(
            doc=field["doc"],
            after_field=field["after_field"],
            field_details=field["field_details"],
            section=field.get("section"),
        )

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()


@click.command("add-commission-expense-account-field")
def add_commission_expense_account_field():
    try:
        frappe.init(site="site.local")
        frappe.connect()
        field = {
            "doc": "Selling Settings",
            "after_field": "territory",
            "field_details": {
                "field_name": "commission_expense_account",
                "field_type": "Link",
                "options": "Account",
                "reqd": 0,
                "label": "Commission Expense Account",
            },
        }

        add_custom_field(
            doc=field["doc"],
            after_field=field["after_field"],
            field_details=field["field_details"],
            section=field.get("section"),
        )

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()


@click.command("add-commission-payable-account-field")
def add_commission_payable_account_field():
    try:
        frappe.init(site="site.local")
        frappe.connect()
        field = {
            "doc": "Selling Settings",
            "after_field": "territory",
            "field_details": {
                "field_name": "commission_payable_account",
                "field_type": "Link",
                "options": "Account",
                "reqd": 0,
                "label": "Commission Payable Account",
            },
        }

        add_custom_field(
            doc=field["doc"],
            after_field=field["after_field"],
            field_details=field["field_details"],
            section=field.get("section"),
        )

    except Exception as e:
        click.echo(f"Error: {str(e)}")
    finally:
        frappe.destroy()

@click.command("add-commission-journal-entry-field")
def add_commission_journal_entry_field():
    try:
        frappe.init(site="site.local")
        frappe.connect()

        field = {
            "doc": "Sales Invoice",
            "after_field": "status",
            "field_details": {
                "fieldname": "commission_journal_entry",
                "fieldtype": "Link",
                "options": "Journal Entry",
                "reqd": 0,
                "label": "Commission Journal Entry",
                "hidden": 1
            },
        }

        add_custom_field(
            doc=field["doc"],
            after_field=field["after_field"],
            field_details=field["field_details"],
            section=field.get("section"),  # Optional, specify a section if needed
        )

        click.echo("Commission Journal Entry field added successfully to Sales Invoice.")

    except Exception as e:
        click.echo(f"Error: {str(e)}")

    finally:
        frappe.destroy() 


# @click.command('add-dashboard-calendar')
# def add_dashboard_calendar():
#     try:
#         frappe.init(site="site.local")
#         frappe.connect()
#         field = {
#         "doc": "Dashboard Chart",
#         "after_field": "has_variants",
#         "field_details": {
#             "field_name": "commission_value",
#             "field_type": "Float",
#             "label": "Commision Value"
#         }}

#         add_custom_field(
#                     doc=field["doc"],
#                     after_field=field["after_field"],
#                     field_details=field["field_details"],
#                     section=field.get("section"),
#                 )

#     except Exception as e:
#         click.echo(f"Error: {str(e)}")
#     finally:
#         frappe.destroy()

commands = [
    create_workspace_command,
    create_column,
    add_commission_on_item,
    add_cost_center_to_user,
    add_commission_expense_account_field,
    add_commission_payable_account_field,
    add_commission_journal_entry_field
]
