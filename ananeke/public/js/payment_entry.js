frappe.ui.form.on("Payment Entry", {
    onload: function (frm) {

        frappe.call({
            method: "frappe.client.get_value",
            args: {
                doctype: "User",
                filters: { name: frappe.session.user },
                fieldname: ["cost_center", "roles"]
            },
            // We should have  checked if we have the correct roles but this works for  now
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
    }
});