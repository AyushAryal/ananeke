// Copyright (c) 2025, Ayush Aryal and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Target", {
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
    },
    refresh: function (frm) {
        compute_progress(frm);
    },
    achieved: function (frm) {
        compute_progress(frm);
    },
    target: function (frm) {
        compute_progress(frm);
    }
});

function compute_progress(frm) {
    if (frm.doc.target && frm.doc.achieved) {
        frm.set_value('progress', (frm.doc.achieved / frm.doc.target) * 100);
    } else {
        frm.set_value('progress', 0);
    }
    frm.save();
};




