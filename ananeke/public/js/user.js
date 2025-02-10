frappe.ui.form.on("User", {
    setup: function (frm) {
        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "User",
                filters: { name: frappe.session.user },
                fieldname: ["roles", "email"]
            },
            callback: function (response) {
                let roles = response.message.roles || [];
                console.log(response.message.roles.includes("Frontdesk"));

                if (!roles.includes("Frontdesk")) {
                    frm.set_df_property('cost_center', 'hidden', 1);
                } else {
                    frm.set_df_property('cost_center', 'hidden', 0);
                }
            }
        });
    }
});
