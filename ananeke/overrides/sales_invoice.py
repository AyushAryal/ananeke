# import frappe
# from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
# from frappe.utils import flt, cint
# from erpnext.accounts.utils import get_account_currency


# class CustomSalesInvoice(SalesInvoice):
#     def make_gl_entries(self, gl_entries=None, from_repost=False):
#         frappe.logger().info(f"Custom make_gl_entries called for Sales Invoice: {self.name}")

#         enable_discount_accounting = cint(
#             frappe.db.get_single_value("Selling Settings", "enable_discount_accounting")
#         )

#         selling_settings = frappe.get_single("Selling Settings")
#         commission_account = selling_settings.commission_account

#         if not commission_account:
#             frappe.throw("Commission account is not set in Selling Settings")

#         for item in self.get("items"):
#             if gl_entries is None:
#                 gl_entries = []
#             commission_value = frappe.db.get_value("Item", {"name": item.item_name}, 'commission_value')
#             if commission_value and item.amount:
#                 commission_amount = flt(item.amount * (commission_value / 100), item.precision("amount"))

#                 amount, base_amount = self.get_amount_and_base_amount(item, enable_discount_accounting)
#                 account_currency = get_account_currency(commission_account)

#                 gl_entries.append(
#                     self.get_gl_dict(
#                         {
#                             "account": commission_account,
#                             "against": self.customer,
#                             "debit": flt(commission_amount, item.precision("base_net_amount")),
#                             "debit_in_account_currency": (
#                                 flt(commission_amount, item.precision("base_net_amount"))
#                                 if account_currency == self.company_currency
#                                 else flt(commission_amount, item.precision("net_amount"))
#                             ),
#                             "cost_center": item.cost_center,
#                             "project": item.project or self.project,
#                         },
#                         account_currency,
#                         item=item,
#                     )
#                 )

#                 # Check if staff_name exists before accessing it
#                 if hasattr(self, "staff_name") and self.staff_name:
#                     gl_entries.append(
#                         self.get_gl_dict(
#                             {
#                                 "account": commission_account,
#                                 "against": self.staff_name,
#                                 "credit": flt(commission_amount, item.precision("base_net_amount")),
#                                 "credit_in_account_currency": (
#                                     flt(commission_amount, item.precision("base_net_amount"))
#                                     if account_currency == self.company_currency
#                                     else flt(commission_amount, item.precision("net_amount"))
#                                 ),
#                                 "cost_center": item.cost_center,
#                                 "project": item.project or self.project,
#                             },
#                             account_currency,
#                             item=item,
#                         )
#                     )

#         if gl_entries:
#             frappe.logger().info(f"GL Entries before posting: {gl_entries}")

#             super().make_gl_entries(gl_entries, from_repost)

#             frappe.logger().info("Custom GL entries have been posted.")
#         else:
#             frappe.logger().info("No GL entries found for posting.")
