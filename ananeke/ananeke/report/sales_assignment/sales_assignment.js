// Copyright (c) 2025, Ayush Aryal and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Assignment"] = {
	"filters": [
		{
            "fieldname": "assign_to",
            "label": __("Sales Person"),
            "fieldtype": "Link",
            "options": "Employee"
        },
		{
            "fieldname": "item",
            "label": __("Item"),
            "fieldtype": "Link",
            "options": "Item"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.nowdate()
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.nowdate()
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer"
        },
        {
            "fieldname": "status",
            "label": __("Status"),
            "fieldtype": "MultiSelectList",
            "options": [
                "Draft",
                "Return",
                "Credit Note Issued",
                "Submitted",
                "Paid",
                "Partly Paid",
                "Unpaid",
                "Unpaid and Discounted",
                "Partly Paid and Discounted",
                "Overdue and Discounted",
                "Overdue",
                "Cancelled",
                "Internal Transfer"
            ],
            "default": ["Paid",]
        },     
        {
            "fieldname": "frequency",
            "label": __("Frequency"),
            "fieldtype": "Select",
            "options": [
                "Daily",
                "Weekly",
                "Monthly",
                "Yearly"
            ],
            "default": "Monthly",
            "on_change": function() {
                update_date_range();
            }
        }
	],
	"frequency": function(report) {
        console.log(report);
        update_date_range();
    }
};

function update_date_range() { set_value(today);
    var frequency = frappe.query_report.filters.find(obj => obj.fieldname === "frequency").value;
    var today = frappe.datetime.nowdate();
    var from_date = "";

    if (frequency === "Daily") {
        from_date = frappe.datetime.add_days(today, -1); 
    } else if (frequency === "Weekly") {
        from_date = frappe.datetime.add_days(today, -7);
    } else if (frequency === "Monthly") {
        from_date = frappe.datetime.add_months(today, -1);
    } else if (frequency === "Yearly") {
        from_date = frappe.datetime.add_days(today, -365);
    }

    var fromDateFilter = frappe.query_report.get_filter("from_date");
    var toDateFilter = frappe.query_report.get_filter("to_date");

    if (fromDateFilter) {
        fromDateFilter.set_value(from_date);
    }
    if (toDateFilter) {
        toDateFilter.set_value(today);
    }

    frappe.query_report.refresh();
}
