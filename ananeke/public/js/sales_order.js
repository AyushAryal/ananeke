frappe.ui.form.on("Sales Order", {
    onload: function (frm) {
        frm.set_df_property('order_type', 'hidden', 1);
        frm.set_df_property('delivery_date', 'hidden', 1);

        if (frm.is_new()) {

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
}
});
