frappe.ui.form.on("SMS Center", {
    onload: function (frm) {
        const urlParams = new URLSearchParams(window.location.search);
        const receivers = urlParams.get('receivers');
        
        if (receivers) {
            const receiver_list_field = frm.fields_dict.receiver_list; 
            if (receiver_list_field) {
                frm.set_value('receiver_list', receivers.split(',').join('\n'));
            }
        }
        }
    
});
