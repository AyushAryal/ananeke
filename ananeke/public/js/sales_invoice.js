frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm){
        if (frm.doc.is_return){
        frm.set_value("naming_series","ACC-SINV-RET-.YYYY.-");
        }
        else{
        frm.set_value("naming_series","ACC-SINV-.YYYY.-")
        }
    },
    is_return: function(frm){
        if (frm.doc.is_return){
        frm.set_value("naming_series","ACC-SINV-RET-.YYYY.-");
        }
        else{
        frm.set_value("naming_series","ACC-SINV-.YYYY.-")
        }
    },
    cost_center: function (frm) {
        if (frm.doc.cost_center) {
            frm.doc.items.forEach((item) => {
                    frappe.model.set_value(
                        item.doctype,
                        item.name,
                        "cost_center",
                        frm.doc.cost_center
                    );
                }
            );       
            frm.refresh_field("items");
        }
    },
    onload: function (frm) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "User",
                filters: { name: frappe.session.user },
                fieldname: ["cost_center", "roles"]
            },
            callback: function (response) {
                if (response) {
                    console.log(response.message);
                    let cost_center = response.message.cost_center;
                    if (cost_center) {
                        frm.set_value("cost_center", cost_center);
                    }
                }
            }
        });
        // frappe.call({
        //     method: "ananeke.methods.employee.check_employee_checked_in_today",
        //     callback: function(r) {
        //         let employeeIds = r.message.map(emp => emp[0]);

        //         if (employeeIds && employeeIds.length > 0) {
        //             frm.fields_dict.items.grid.get_field("assign_to").get_query = function(doc) {
        //                 return {
        //                     filters: {
        //                         employee: ["in", employeeIds]
        //                     }
        //                 };
        //             };
        //             frm.refresh_fields();
        //         } else {
        //             frm.fields_dict.items.grid.get_field("assign_to").get_query = function(doc) {
        //                 return {
        //                     filters: {
        //                         employee: ["in", []]
        //                     }
        //                 };
        //             };
        //             frm.refresh_fields();
        //         }
        //     },
        //     error: function(err) {
        //         frappe.msgprint(__('Error fetching employees: ') + err);
        //     }
        // });
        frm.set_query("offsetting_account", "dimension_defaults", function (doc, cdt, cdn) {
			let d = locals[cdt][cdn];
			return {
				filters: {
					company: d.company,
					root_type: ["in", ["Asset", "Liability"]],
					is_group: 0,
				},
			};
		});
    }
});


// frappe.ui.form.on('Sales Invoice Item', {
//     refresh: function (frm, cdt, cdn) {
//         let row = frappe.get_doc(cdt, cdn);
//         let employee = row.assign_to; 
//         console.log(employee);

        
//     },
// });
