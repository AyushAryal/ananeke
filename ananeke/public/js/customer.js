frappe.ui.form.on('Customer', {
	onload: function (frm) {
        if (frm.is_quick_entry) {
            frm.set_df_property('mobile_no', 'reqd', 1);
        }
    },
    refresh: function(frm) {
            frm.add_custom_button(__('Book Appointment'), function() {
					frappe.model.open_mapped_doc({
						method: 'ananeke.methods.sales_order.make_appointment',
						frm: frm,
					});
				}).addClass("btn-primary");
    }
})