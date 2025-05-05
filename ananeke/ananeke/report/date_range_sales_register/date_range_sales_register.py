# Copyright (c) 2025, Ayush Marhatta and contributors
# For license information, please see license.txt


import frappe
from frappe import _, msgprint
from frappe.model.meta import get_field_precision
from frappe.query_builder.custom import ConstantColumn
from frappe.utils import flt, getdate
from pypika import Order

from erpnext.accounts.party import get_party_account
from erpnext.accounts.report.utils import (
    filter_invoices_based_on_dimensions,
    get_advance_taxes_and_charges,
    get_journal_entries,
    get_opening_row,
    get_party_details,
    get_payment_entries,
    get_query_columns,
    get_taxes_query,
    get_values_for_columns,
)


def execute(filters=None):
    return _execute(filters)


def _execute(filters, additional_table_columns=None):
    if not filters:
        filters = frappe._dict({})

    include_payments = filters.get("include_payments")
    if filters.get("include_payments") and not filters.get("customer"):
        frappe.throw(_("Please select a customer for fetching payments."))
    invoice_list = get_invoices(filters, get_query_columns(additional_table_columns))
    if filters.get("include_payments"):
        invoice_list += get_payments(filters)

    columns, income_accounts, unrealized_profit_loss_accounts, tax_accounts = (
        get_columns(invoice_list, additional_table_columns, include_payments)
    )

    if not invoice_list:
        msgprint(_("No record found"))
        return columns, invoice_list

    invoice_income_map = get_invoice_income_map(invoice_list)
    internal_invoice_map = get_internal_invoice_map(invoice_list)
    invoice_income_map, invoice_tax_map = get_invoice_tax_map(
        invoice_list, invoice_income_map, income_accounts, include_payments
    )
    invoice_cc_wh_map = get_invoice_cc_wh_map(invoice_list)
    invoice_so_dn_map = get_invoice_so_dn_map(invoice_list)
    company_currency = frappe.get_cached_value(
        "Company", filters.get("company"), "default_currency"
    )
    mode_of_payment_details = get_mode_of_payment_details(
        [inv.name for inv in invoice_list]
    )
    customers = list(set(d.customer for d in invoice_list))
    customer_details = get_party_details("Customer", customers)

    data = []
    for inv in invoice_list:
        payment_entries = mode_of_payment_details.get(inv.name, [])

        if filters.get("mode_of_payment"):
            # Filter payment entries for specific mode of payment
            payment_entries = [
                (mode, amount)
                for mode, amount in payment_entries
                if mode == filters.get("mode_of_payment")
            ]

            # Skip if no matching payment mode
            if not payment_entries:
                continue

        # Get base row data
        base_row = get_base_row_data(
            inv,
            invoice_so_dn_map,
            invoice_cc_wh_map,
            customer_details,
            additional_table_columns,
            company_currency,
        )

        if not payment_entries:
            # If no payment entries, create a single row with empty mode of payment
            row = base_row.copy()
            row.update(
                get_amount_details(
                    inv,
                    invoice_income_map,
                    internal_invoice_map,
                    invoice_tax_map,
                    income_accounts,
                    tax_accounts,
                    unrealized_profit_loss_accounts,
                    company_currency,
                )
            )
            data.append(row)
        else:
            # Create separate rows for each mode of payment
            for payment_mode, paid_amount in payment_entries:
                row = base_row.copy()
                row["mode_of_payment"] = payment_mode

                # Calculate proportional amounts based on payment ratio
                payment_ratio = (
                    flt(paid_amount) / flt(inv.base_grand_total)
                    if inv.base_grand_total
                    else 0
                )
                amount_details = get_amount_details(
                    inv,
                    invoice_income_map,
                    internal_invoice_map,
                    invoice_tax_map,
                    income_accounts,
                    tax_accounts,
                    unrealized_profit_loss_accounts,
                    company_currency,
                    payment_ratio,
                )
                row.update(amount_details)
                data.append(row)

    return columns, sorted(
        data, key=lambda x: (x["posting_date"], x.get("mode_of_payment", ""))
    )


def get_columns(invoice_list, additional_table_columns, include_payments=False):
    """return columns based on filters"""
    columns = [
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 160,
        },
        {
            "label": _("Voucher"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 200,
        },
    ]

    if additional_table_columns and not include_payments:
        columns += additional_table_columns

    if not include_payments:
        columns += [
            # {
            #     "label": _("Customer Group"),
            #     "fieldname": "customer_group",
            #     "fieldtype": "Link",
            #     "options": "Customer Group",
            #     "width": 120,
            # },
            # {
            #     "label": _("Territory"),
            #     "fieldname": "territory",
            #     "fieldtype": "Link",
            #     "options": "Territory",
            #     "width": 80,
            # },
            # {
            #     "label": _("Tax Id"),
            #     "fieldname": "tax_id",
            #     "fieldtype": "Data",
            #     "width": 80,
            # },
            # {
            #     "label": _("Receivable Account"),
            #     "fieldname": "receivable_account",
            #     "fieldtype": "Link",
            #     "options": "Account",
            #     "width": 100,
            # },
            {
                "label": _("Mode Of Payment"),
                "fieldname": "mode_of_payment",
                "fieldtype": "Data",
                "width": 120,
            },
            # {
            #     "label": _("Project"),
            #     "fieldname": "project",
            #     "fieldtype": "Link",
            #     "options": "Project",
            #     "width": 80,
            # },
            # {
            #     "label": _("Sales Order"),
            #     "fieldname": "sales_order",
            #     "fieldtype": "Link",
            #     "options": "Sales Order",
            #     "width": 100,
            # },
            # {
            #     "label": _("Delivery Note"),
            #     "fieldname": "delivery_note",
            #     "fieldtype": "Link",
            #     "options": "Delivery Note",
            #     "width": 100,
            # },
            {
                "label": _("Cost Center"),
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "options": "Cost Center",
                "width": 200,
            },
            # {
            #     "label": _("Warehouse"),
            #     "fieldname": "warehouse",
            #     "fieldtype": "Link",
            #     "options": "Warehouse",
            #     "width": 100,
            # },
            # {
            #     "fieldname": "currency",
            #     "label": _("Currency"),
            #     "fieldtype": "Data",
            #     "width": 80,
            # },
            {
                "label": _("Owner"),
                "fieldname": "owner",
                "fieldtype": "Data",
                "width": 160,
            },
        ]
    else:
        columns += [
            # {
            #     "fieldname": "receivable_account",
            #     "label": _("Receivable Account"),
            #     "fieldtype": "Link",
            #     "options": "Account",
            #     "width": 120,
            # },
            # {
            #     "fieldname": "debit",
            #     "label": _("Debit"),
            #     "fieldtype": "Currency",
            #     "width": 120,
            # },
            # {
            #     "fieldname": "credit",
            #     "label": _("Credit"),
            #     "fieldtype": "Currency",
            #     "width": 120,
            # },
            # {
            #     "fieldname": "balance",
            #     "label": _("Balance"),
            #     "fieldtype": "Currency",
            #     "width": 120,
            # },
        ]

    account_columns, accounts = get_account_columns(invoice_list, include_payments)

    net_total_column = [
        {
            "label": _("Net Total"),
            "fieldname": "net_total",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        }
    ]

    total_columns = [
        # {
        #     "label": _("Tax Total"),
        #     "fieldname": "tax_total",
        #     "fieldtype": "Currency",
        #     "options": "currency",
        #     "width": 120,
        # }
    ]
    if not include_payments:
        total_columns += [
            # {
            #     "label": _("Grand Total"),
            #     "fieldname": "grand_total",
            #     "fieldtype": "Currency",
            #     "options": "currency",
            #     "width": 120,
            # },
            # {
            #     "label": _("Rounded Total"),
            #     "fieldname": "rounded_total",
            #     "fieldtype": "Currency",
            #     "options": "currency",
            #     "width": 120,
            # },
            # {
            #     "label": _("Outstanding Amount"),
            #     "fieldname": "outstanding_amount",
            #     "fieldtype": "Currency",
            #     "options": "currency",
            #     "width": 120,
            # },
        ]

    columns = (
        columns
        # + account_columns[0]
        # + account_columns[2]
        + net_total_column
        # + account_columns[1]
        + total_columns
    )
    columns += [
        # {
        #     "label": _("Remarks"),
        #     "fieldname": "remarks",
        #     "fieldtype": "Data",
        #     "width": 150,
        # }
    ]
    return columns, accounts[0], accounts[1], accounts[2]


def get_account_columns(invoice_list, include_payments):
    income_accounts = []
    tax_accounts = []
    unrealized_profit_loss_accounts = []

    income_columns = []
    tax_columns = []
    unrealized_profit_loss_account_columns = []

    if invoice_list:
        income_accounts = frappe.db.sql_list(
            """select distinct income_account
			from `tabSales Invoice Item` where docstatus = 1 and parent in (%s)
			order by income_account"""
            % ", ".join(["%s"] * len(invoice_list)),
            tuple(inv.name for inv in invoice_list),
        )

        sales_taxes_query = get_taxes_query(
            invoice_list, "Sales Taxes and Charges", "Sales Invoice"
        )
        sales_tax_accounts = sales_taxes_query.run(as_dict=True, pluck="account_head")
        tax_accounts = sales_tax_accounts

        if include_payments:
            advance_taxes_query = get_taxes_query(
                invoice_list, "Advance Taxes and Charges", "Payment Entry"
            )
            advance_tax_accounts = advance_taxes_query.run(
                as_dict=True, pluck="account_head"
            )
            tax_accounts = set(tax_accounts + advance_tax_accounts)

        unrealized_profit_loss_accounts = frappe.db.sql_list(
            """SELECT distinct unrealized_profit_loss_account
			from `tabSales Invoice` where docstatus = 1 and name in (%s)
			and is_internal_customer = 1
			and ifnull(unrealized_profit_loss_account, '') != ''
			order by unrealized_profit_loss_account"""
            % ", ".join(["%s"] * len(invoice_list)),
            tuple(inv.name for inv in invoice_list),
        )

    for account in income_accounts:
        income_columns.append(
            {
                "label": account,
                "fieldname": frappe.scrub(account),
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            }
        )

    for account in tax_accounts:
        if account not in income_accounts:
            tax_columns.append(
                {
                    "label": account,
                    "fieldname": frappe.scrub(account),
                    "fieldtype": "Currency",
                    "options": "currency",
                    "width": 120,
                }
            )

    for account in unrealized_profit_loss_accounts:
        unrealized_profit_loss_account_columns.append(
            {
                "label": account,
                "fieldname": frappe.scrub(account + "_unrealized"),
                "fieldtype": "Currency",
                "options": "currency",
                "width": 120,
            }
        )

    columns = [income_columns, unrealized_profit_loss_account_columns, tax_columns]
    accounts = [income_accounts, unrealized_profit_loss_accounts, tax_accounts]

    return columns, accounts


def get_invoices(filters, additional_query_columns):
    si = frappe.qb.DocType("Sales Invoice")
    query = (
        frappe.qb.from_(si)
        .select(
            ConstantColumn("Sales Invoice").as_("doctype"),
            si.name,
            si.posting_date,
            si.debit_to,
            si.project,
            si.customer,
            si.customer_name,
            si.owner,
            si.remarks,
            si.territory,
            si.tax_id,
            si.customer_group,
            si.base_net_total,
            si.base_grand_total,
            si.base_rounded_total,
            si.outstanding_amount,
            si.is_internal_customer,
            si.represents_company,
            si.company,
            si.cost_center,
        )
        .where(si.docstatus == 1)
        .orderby(si.posting_date, si.name, order=Order.desc)
    )

    if additional_query_columns:
        for col in additional_query_columns:
            query = query.select(col)

    if filters.get("customer"):
        query = query.where(si.customer == filters.customer)

    query = get_conditions(filters, query, "Sales Invoice")
    query = apply_common_conditions(
        filters, query, doctype="Sales Invoice", child_doctype="Sales Invoice Item"
    )

    invoices = query.run(as_dict=True)
    return invoices


def apply_common_conditions(
    filters, query, doctype, child_doctype=None, payments=False
):
    parent_doc = frappe.qb.DocType(doctype)
    if child_doctype:
        child_doc = frappe.qb.DocType(child_doctype)

    join_required = False

    if filters.get("company"):
        query = query.where(parent_doc.company == filters.company)
    if filters.get("from_date"):
        query = query.where(parent_doc.posting_date >= filters.from_date)
    if filters.get("to_date"):
        query = query.where(parent_doc.posting_date <= filters.to_date)

    if payments:
        if doctype == "Journal Entry" and filters.get("cost_center"):
            query = query.where(child_doc.cost_center == filters.cost_center)
        elif filters.get("cost_center"):
            query = query.where(parent_doc.cost_center == filters.cost_center)
    else:
        if filters.get("cost_center"):
            if child_doctype:
                query = query.where(
                    (
                        parent_doc.cost_center == filters.cost_center
                    )  # Prioritize Sales Invoice Cost Center
                    | (
                        parent_doc.cost_center.isnull() & child_doc.cost_center
                        == filters.cost_center
                    )  # Use Item Cost Center if missing
                )
                join_required = True
            else:
                query = query.where(parent_doc.cost_center == filters.cost_center)
        if filters.get("warehouse"):
            query = query.where(child_doc.warehouse == filters.warehouse)
            join_required = True
        if filters.get("item_group"):
            query = query.where(child_doc.item_group == filters.item_group)
            join_required = True

    if not payments:
        if filters.get("brand"):
            query = query.where(child_doc.brand == filters.brand)
            join_required = True

    if join_required:
        query = query.inner_join(child_doc).on(parent_doc.name == child_doc.parent)
        query = query.where(child_doc.parenttype == doctype)
        query = query.distinct()

    if parent_doc.get_table_name() != "tabJournal Entry":
        query = filter_invoices_based_on_dimensions(filters, query, parent_doc)

    return query


def get_conditions(filters, query, doctype):
    parent_doc = frappe.qb.DocType(doctype)
    if filters.get("owner"):
        query = query.where(parent_doc.owner == filters.owner)

    if filters.get("from_date"):
        query = query.where(parent_doc.posting_date >= filters.from_date)
    if filters.get("to_date"):
        query = query.where(parent_doc.posting_date <= filters.to_date)

    if filters.get("company"):
        query = query.where(parent_doc.company == filters.company)

    if filters.get("mode_of_payment"):
        sip_doc = frappe.qb.DocType("Sales Invoice Payment")
        per_doc = frappe.qb.DocType("Payment Entry Reference")
        pe_doc = frappe.qb.DocType("Payment Entry")

        query = query.where(
            (
                parent_doc.name.isin(
                    frappe.qb.from_(sip_doc)
                    .select(sip_doc.parent)
                    .where(sip_doc.mode_of_payment == filters.mode_of_payment)
                )
            )
            | (
                parent_doc.name.isin(
                    frappe.qb.from_(per_doc)
                    .join(pe_doc)
                    .on(per_doc.parent == pe_doc.name)
                    .select(per_doc.reference_name)
                    .where(
                        (per_doc.reference_doctype == "Sales Invoice")
                        & (pe_doc.mode_of_payment == filters.mode_of_payment)
                    )
                )
            )
        )

    return query


def get_payments(filters):
    args = frappe._dict(
        account="debit_to",
        account_fieldname="paid_from",
        party="customer",
        party_name="customer_name",
        party_account=get_party_account(
            "Customer", filters.customer, filters.company, include_advance=True
        ),
    )
    payment_entries = get_payment_entries(filters, args)
    journal_entries = get_journal_entries(filters, args)
    return payment_entries + journal_entries


def get_invoice_income_map(invoice_list):
    income_details = frappe.db.sql(
        """select parent, income_account, sum(base_net_amount) as amount
		from `tabSales Invoice Item` where parent in (%s) group by parent, income_account"""
        % ", ".join(["%s"] * len(invoice_list)),
        tuple(inv.name for inv in invoice_list),
        as_dict=1,
    )

    invoice_income_map = {}
    for d in income_details:
        invoice_income_map.setdefault(d.parent, frappe._dict()).setdefault(
            d.income_account, []
        )
        invoice_income_map[d.parent][d.income_account] = flt(d.amount)

    return invoice_income_map


def get_internal_invoice_map(invoice_list):
    unrealized_amount_details = frappe.db.sql(
        """SELECT name, unrealized_profit_loss_account,
		base_net_total as amount from `tabSales Invoice` where name in (%s)
		and is_internal_customer = 1 and company = represents_company"""
        % ", ".join(["%s"] * len(invoice_list)),
        tuple(inv.name for inv in invoice_list),
        as_dict=1,
    )

    internal_invoice_map = {}
    for d in unrealized_amount_details:
        if d.unrealized_profit_loss_account:
            internal_invoice_map.setdefault(
                (d.name, d.unrealized_profit_loss_account), d.amount
            )

    return internal_invoice_map


def get_invoice_tax_map(
    invoice_list, invoice_income_map, income_accounts, include_payments=False
):
    tax_details = frappe.db.sql(
        """select parent, account_head,
		sum(base_tax_amount_after_discount_amount) as tax_amount
		from `tabSales Taxes and Charges` where parent in (%s) and parenttype = 'Sales Invoice'
		group by parent, account_head"""
        % ", ".join(["%s"] * len(invoice_list)),
        tuple(inv.name for inv in invoice_list),
        as_dict=1,
    )

    if include_payments:
        tax_details += get_advance_taxes_and_charges(invoice_list)

    invoice_tax_map = {}
    for d in tax_details:
        if d.account_head in income_accounts:
            if d.account_head in invoice_income_map[d.parent]:
                invoice_income_map[d.parent][d.account_head] += flt(d.tax_amount)
            else:
                invoice_income_map[d.parent][d.account_head] = flt(d.tax_amount)
        else:
            invoice_tax_map.setdefault(d.parent, frappe._dict()).setdefault(
                d.account_head, []
            )
            invoice_tax_map[d.parent][d.account_head] = flt(d.tax_amount)

    return invoice_income_map, invoice_tax_map


def get_invoice_so_dn_map(invoice_list):
    si_items = frappe.db.sql(
        """select parent, sales_order, delivery_note, so_detail
		from `tabSales Invoice Item` where parent in (%s)
		and (sales_order != '' or delivery_note != '')"""
        % ", ".join(["%s"] * len(invoice_list)),
        tuple(inv.name for inv in invoice_list),
        as_dict=1,
    )

    invoice_so_dn_map = {}
    for d in si_items:
        if d.sales_order:
            invoice_so_dn_map.setdefault(d.parent, frappe._dict()).setdefault(
                "sales_order", []
            ).append(d.sales_order)

        delivery_note_list = None
        if d.delivery_note:
            delivery_note_list = [d.delivery_note]
        elif d.sales_order:
            delivery_note_list = frappe.db.sql_list(
                """select distinct parent from `tabDelivery Note Item`
				where docstatus=1 and so_detail=%s""",
                d.so_detail,
            )

        if delivery_note_list:
            invoice_so_dn_map.setdefault(d.parent, frappe._dict()).setdefault(
                "delivery_note", delivery_note_list
            )

    return invoice_so_dn_map


# def get_invoice_cc_wh_map(invoice_list):
#     si_items = frappe.db.sql(
#         """select parent, cost_center, warehouse
# 		from `tabSales Invoice Item` where parent in (%s)
# 		and (cost_center != '' or warehouse != '')"""
#         % ", ".join(["%s"] * len(invoice_list)),
#         tuple(inv.name for inv in invoice_list),
#         as_dict=1,
#     )

#     invoice_cc_wh_map = {}
#     for d in si_items:
#         if d.cost_center:
#             invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
#                 "cost_center", []
#             ).append(d.cost_center)

#         if d.warehouse:
#             invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
#                 "warehouse", []
#             ).append(d.warehouse)

#     return invoice_cc_wh_map


def get_invoice_cc_wh_map(invoice_list):
    si_items = frappe.db.sql(
        """SELECT parent, cost_center, warehouse
        FROM `tabSales Invoice Item` 
        WHERE parent IN (%s) AND (cost_center != '' OR warehouse != '')"""
        % ", ".join(["%s"] * len(invoice_list)),
        tuple(inv.name for inv in invoice_list),
        as_dict=1,
    )

    si_cost_centers = frappe.db.sql(
        """SELECT name, cost_center 
        FROM `tabSales Invoice`
        WHERE name IN (%s)"""
        % ", ".join(["%s"] * len(invoice_list)),
        tuple(inv.name for inv in invoice_list),
        as_dict=1,
    )

    invoice_cc_wh_map = {}
    for si in si_cost_centers:
        invoice_cc_wh_map.setdefault(si.name, frappe._dict())["cost_center"] = (
            [si.cost_center] if si.cost_center else []
        )

    for d in si_items:
        if not invoice_cc_wh_map.get(d.parent, {}).get(
            "cost_center"
        ):  # Only add if not set at invoice level
            invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
                "cost_center", []
            ).append(d.cost_center)

        if d.warehouse:
            invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
                "warehouse", []
            ).append(d.warehouse)

    return invoice_cc_wh_map


def get_mode_of_payments(invoice_list):
    mode_of_payments = {}
    if invoice_list:
        inv_mop = frappe.db.sql(
            """select parent, mode_of_payment
			from `tabSales Invoice Payment`
            where parent in (%s) 
            group by parent, mode_of_payment"""
            % ", ".join(["%s"] * len(invoice_list)),
            tuple(invoice_list),
            as_dict=1,
        )

        for d in inv_mop:
            if d.mode_of_payment:
                mode_of_payments.setdefault(d.parent, []).append(d.mode_of_payment)

        payment_mop = frappe.db.sql(
            """select per.reference_name as invoice, pe.mode_of_payment 
               from `tabPayment Entry Reference` per
               join `tabPayment Entry` pe on pe.name = per.parent
               where per.reference_doctype = 'Sales Invoice'
               and per.reference_name in (%s)
               group by per.reference_name, pe.mode_of_payment"""
            % ", ".join(["%s"] * len(invoice_list)),
            tuple(invoice_list),
            as_dict=1,
        )

        for d in payment_mop:
            if d.mode_of_payment:
                mode_of_payments.setdefault(d.invoice, []).append(d.mode_of_payment)

    return mode_of_payments


def get_mode_of_payment_details(invoice_list):
    mode_of_payments = {}
    if invoice_list:
        inv_mop = frappe.db.sql(
            """select parent, mode_of_payment, base_amount as paid_amount
            from `tabSales Invoice Payment`
            where parent in (%s)
            group by parent, mode_of_payment"""
            % ", ".join(["%s"] * len(invoice_list)),
            tuple(invoice_list),
            as_dict=1,
        )

        for d in inv_mop:
            if d.mode_of_payment:
                mode_of_payments.setdefault(d.parent, []).append(
                    (d.mode_of_payment, d.paid_amount)
                )

        payment_mop = frappe.db.sql(
            """select per.reference_name as parent, pe.mode_of_payment, 
                   per.allocated_amount as paid_amount
            from `tabPayment Entry Reference` per
            join `tabPayment Entry` pe on pe.name = per.parent
            where per.reference_doctype = 'Sales Invoice'
            and per.reference_name in (%s)
            group by per.reference_name, pe.mode_of_payment"""
            % ", ".join(["%s"] * len(invoice_list)),
            tuple(invoice_list),
            as_dict=1,
        )

        for d in payment_mop:
            if d.mode_of_payment:
                mode_of_payments.setdefault(d.parent, []).append(
                    (d.mode_of_payment, d.paid_amount)
                )

    return mode_of_payments


def get_base_row_data(
    inv,
    invoice_so_dn_map,
    invoice_cc_wh_map,
    customer_details,
    additional_table_columns,
    company_currency,
):
    sales_order = list(set(invoice_so_dn_map.get(inv.name, {}).get("sales_order", [])))
    delivery_note = list(
        set(invoice_so_dn_map.get(inv.name, {}).get("delivery_note", []))
    )
    cost_center = list(set(invoice_cc_wh_map.get(inv.name, {}).get("cost_center", [])))
    warehouse = list(set(invoice_cc_wh_map.get(inv.name, {}).get("warehouse", [])))
    inv_customer_details = customer_details.get(inv.customer, {})

    return {
        "voucher_type": inv.doctype,
        "voucher_no": inv.name,
        "posting_date": inv.posting_date,
        "customer": inv.customer,
        "customer_name": inv.customer_name,
        **get_values_for_columns(additional_table_columns, inv),
        "customer_group": inv_customer_details.get("customer_group"),
        "territory": inv_customer_details.get("territory"),
        "tax_id": inv_customer_details.get("tax_id"),
        "receivable_account": inv.debit_to,
        "project": inv.project,
        "owner": inv.owner,
        "remarks": inv.remarks,
        "sales_order": ", ".join(sales_order),
        "delivery_note": ", ".join(delivery_note),
        "cost_center": ", ".join(cost_center),
        "warehouse": ", ".join(warehouse),
        "currency": company_currency,
    }


def get_amount_details(
    inv,
    invoice_income_map,
    internal_invoice_map,
    invoice_tax_map,
    income_accounts,
    tax_accounts,
    unrealized_profit_loss_accounts,
    company_currency,
    payment_ratio=1,
):
    row = {}
    base_net_total = 0

    # map income values
    for income_acc in income_accounts:
        if inv.is_internal_customer and inv.company == inv.represents_company:
            income_amount = 0
        else:
            income_amount = flt(invoice_income_map.get(inv.name, {}).get(income_acc))

        income_amount = flt(income_amount * payment_ratio)
        base_net_total += income_amount
        row.update({frappe.scrub(income_acc): income_amount})

    # Add amount in unrealized account
    for account in unrealized_profit_loss_accounts:
        unrealized_amount = (
            flt(internal_invoice_map.get((inv.name, account))) * payment_ratio
        )
        row.update({frappe.scrub(account + "_unrealized"): unrealized_amount})

    # net total
    row.update({"net_total": base_net_total or (inv.base_net_total * payment_ratio)})

    # tax account
    total_tax = 0
    for tax_acc in tax_accounts:
        if tax_acc not in income_accounts:
            tax_amount_precision = (
                get_field_precision(
                    frappe.get_meta("Sales Taxes and Charges").get_field("tax_amount"),
                    currency=company_currency,
                )
                or 2
            )
            tax_amount = flt(
                invoice_tax_map.get(inv.name, {}).get(tax_acc), tax_amount_precision
            )
            tax_amount = flt(tax_amount * payment_ratio)
            total_tax += tax_amount
            row.update({frappe.scrub(tax_acc): tax_amount})

    # total tax, grand total, outstanding amount & rounded total
    grand_total = flt(inv.base_grand_total * payment_ratio)
    row.update(
        {
            "tax_total": total_tax,
            "grand_total": grand_total,
            "rounded_total": flt(inv.base_rounded_total * payment_ratio),
            "outstanding_amount": flt(inv.outstanding_amount * payment_ratio),
        }
    )

    if inv.doctype == "Sales Invoice":
        row.update({"debit": grand_total, "credit": 0.0})
    else:
        row.update({"debit": 0.0, "credit": grand_total})

    return row
