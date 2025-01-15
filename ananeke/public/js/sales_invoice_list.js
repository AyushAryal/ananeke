frappe.listview_settings['Sales Invoice'] = {
    onload: function (listview) {
        listview.page.add_inner_button('Message Selections', () => {
            const selected_items = listview.get_checked_items();
            
            // If no invoices are selected, show a message
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
                    invoices: selected_names, // Pass invoice IDs
                },
                callback: function (r) {
                    if (r && r.message) {
                        // Ensure r.message.contacts is an array
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
            
                    // Redirect with the numbers
                    window.location.href = `/app/sms-center?receivers=${encodeURIComponent(customer_numbers.join(','))}`;
                }
            });
            
        
        });
    },
};
