frappe.ui.form.on('Customer', {
    refresh: function(frm) {
            frm.add_custom_button(__('Book Appointment'), function() {
					frappe.model.open_mapped_doc({
						method: 'ananeke.methods.sales_order.make_appointment',
						frm: frm,
					});
				}).addClass("btn-primary");
    }
})