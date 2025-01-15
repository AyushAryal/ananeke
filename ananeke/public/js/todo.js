frappe.ui.form.on("ToDo", {
    setup: function (frm) {
        frm.set_df_property('date', 'hidden', 1);
    }
})