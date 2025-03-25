// Copyright (c) 2025, Ayush Aryal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Target", {
    refresh: function(frm) {
        frappe.msgprint(frm.doc.status);
    },
    before_save: function(frm) {
        if (frm.doc.employee) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Employee',
                    name: frm.doc.employee
                },
                callback: function(r) {
                    if (r.message) {
                        var full_name = r.message.employee_name;
                        frm.set_value('employee_name', full_name);
                    }
                }
            });
        }
    }
});




