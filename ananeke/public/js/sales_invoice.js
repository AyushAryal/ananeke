frappe.ui.form.on("Sales Invoice", {

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
            // Should have checked if we have the correct roles but this works for  now
            callback: function (response) {
                if (response) {
                    let cost_center = response.message.cost_center;
                    if (cost_center) {
                        frm.set_value("cost_center", cost_center);
                    }
                }
            }
        });
    }
});