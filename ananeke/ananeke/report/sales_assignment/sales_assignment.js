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
            "default": frappe.datetime.add_days(frappe.datetime.nowdate(), -30)
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
        update_date_range();
    }
};

function update_date_range() {
	console.log("yaad");
    // var frequency = frappe.query_reports.filters_dict.frequency.get_value();
	console.log(frappe.query_report)
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

    frappe.query_report.filters_dict.from_date.set_value(from_date);
    frappe.query_report.filters_dict.to_date.set_value(today);
    frappe.query_report.refresh();
}
