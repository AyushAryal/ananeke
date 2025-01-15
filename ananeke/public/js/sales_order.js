frappe.ui.form.on("Sales Order", {
    setup: function (frm) {
        frm.set_df_property('order_type', 'hidden', 1);
        frm.set_df_property('delivery_date', 'hidden', 1);

    }
})