frappe.listview_settings['Sales Invoice'] = {
    get_indicator: function (doc) {
		const status_colors = {
			Draft: "red",
			Unpaid: "orange",
			Paid: "green",
			Return: "gray",
			"Credit Note Issued": "gray",
			"Unpaid and Discounted": "orange",
			"Partly Paid and Discounted": "yellow",
			"Overdue and Discounted": "red",
			Overdue: "red",
			"Partly Paid": "yellow",
			"Internal Transfer": "darkgrey",
		};
		return [__(doc.status), status_colors[doc.status], "status,=," + doc.status];
	},
    onload: function (listview) {
        
        listview.page.add_inner_button('Message Selections', () => {
            const selected_items = listview.get_checked_items();
            
            if (!selected_items.length) {
                frappe.msgprint({
                    title: __('No Selection'),
                    indicator: 'orange',
                    message: __('Please select at least one Sales Invoice.'),
                });
                return;
            }

            const selected_names = selected_items.map(item => item.name);

            let customer_numbers = [];

            frappe.call({
                method: "ananeke.methods.sales_invoice.get_customer_numbers",
                args: {
                    invoices: selected_names,
                },
                callback: function (r) {
                    if (r && r.message) {
                        if (Array.isArray(r.message.contacts) && r.message.contacts.length > 0) {
                            customer_numbers.push(...r.message.contacts); // Add contacts to the customer_numbers array
                        }
                    }
            
                    if (!customer_numbers.length) {
                        frappe.msgprint({
                            title: __('No Phone Numbers'),
                            indicator: 'red',
                            message: __('No valid customer phone numbers found in the selected Sales Invoices.'),
                        });
                        return;
                    }
                    window.location.href = `/app/sms-center?receivers=${encodeURIComponent(customer_numbers.join(','))}`;
                }
            });
        });
    },
};
