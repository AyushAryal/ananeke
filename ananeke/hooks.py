app_name = "ananeke"
app_title = "Ananeke"
app_publisher = "Ayush Aryal"
app_description = "Ananeke modifications"
app_email = "ayusharyal100@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ananeke",
# 		"logo": "/assets/ananeke/logo.png",
# 		"title": "Ananeke",
# 		"route": "/ananeke",
# 		"has_permission": "ananeke.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------
website_route_rules = [
    {"from_route": "/sms-center", "to_route": "sms_center"}
]
# include js, css files in header of desk.html
app_include_css = "/assets/ananeke/css/ananeke_styles.css"
app_include_js = ["/assets/ananeke/js/notification.js",
                  "/assets/ananeke/js/pos.js",
                  ]
# app_include_js = "/assets/ananeke/js/ananeke.js"

# include js, css files in header of web template
# web_include_css = "/assets/ananeke/css/ananeke.css"
# web_include_js = "/assets/ananeke/js/ananeke.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ananeke/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
# page_js = {"page" : "public/js/custom.js",
#            "point-of-sale": "public/js/pos.js"}

# include js in doctype views
doctype_js = {"Sales Order" : "public/js/sales_order.js",
              "Sales Invoice" : "public/js/sales_invoice.js",
              "Payment Entry" : "public/js/payment_entry.js",
              "SMS Center": "public/js/sms_center.js",
              "Employee": "public/js/employee.js",
              "Employee Target": "public/js/employee_target.js",
              "Customer": "public/js/customer.js",
              "User": "public/js/user.js",
              "Stock Entry": "public/js/stock_entry.js",
              "ToDo": "public/js/todo.js"}

doctype_list_js = {"Sales Invoice" : "public/js/sales_invoice_list.js",
                   "Sales Order": "public/js/sales_order_list.js",
                   "Customer": "public/js/customer_list.js",
                   "ToDo": "public/js/todo_listview.js"
                   }
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

doctype_calendar_js = {"Sales Order" : "public/js/sales_order_calendar.js",
                       "ToDo" : "public/js/todo_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ananeke/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ananeke.utils.jinja_methods",
# 	"filters": "ananeke.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ananeke.install.before_install"
after_install = "ananeke.install.after_install"

# Uninstallation
# ------------

before_uninstall = "ananeke.uninstall.before_uninstall"
# after_uninstall = "ananeke.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ananeke.utils.before_app_install"
# after_app_install = "ananeke.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ananeke.utils.before_app_uninstall"
# after_app_uninstall = "ananeke.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ananeke.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"Sales Invoice": "ananeke.overrides.sales_invoice.CustomSalesInvoice"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Stock Entry": {
		"before_save": "ananeke.overrides.stock_entry.stock_entry",
	},
	"Sales Order": {
		"on_submit": "ananeke.methods.sales_order.sales_order",
	},
    "Sales Invoice": {
		"on_cancel": "ananeke.methods.sales_invoice.sales_invoice",
		"on_submit": "ananeke.methods.sales_invoice.sales_invoice",
	# 	"before_save": "ananeke.methods.sales_invoice.sales_invoice",
	},
    "ToDo": {
		"before_save": "ananeke.methods.todo.todo",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ananeke.tasks.all"
# 	],
# 	"daily": [
# 		"ananeke.tasks.daily"
# 	],
# 	"hourly": [
# 		"ananeke.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ananeke.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ananeke.tasks.monthly"
# 	],
# }

# Testing
# -------
# fixtures = [
#     {
#         "dt": "Role",
#         "filters": [["name", "=", "Frontdesk"]]
#     },
#     {
#         "dt": "Custom DocPerm",
#         "filters": [["role", "=", "Frontdesk"]]
#     }
# ]
# before_tests = "ananeke.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ananeke.event.get_events"
# }
#
override_whitelisted_methods = {
    "frappe.desk.listview.get_list_view_fields": "ananeke.overrides.todo_override.custom_get_list_view_fields",
    # "erpnext.accounts.doctype.sales_invoice.sales_invoice.SalesInvoice": "ananeke.overrides.sales_invoice.CustomSalesInvoice"
}

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ananeke.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ananeke.utils.before_request"]
# after_request = ["ananeke.utils.after_request"]

# Job Events
# ----------
# before_job = ["ananeke.utils.before_job"]
# after_job = ["ananeke.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ananeke.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

