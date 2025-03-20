frappe.ui.form.on("ToDo", {
    refresh: function(frm) {
        let previewBlock = $('.preview-block');
        let allocated_to = frm.doc.allocated_to;
        let service_datetime = frm.doc.start_date_time || "Not Set";

        let formattedDate = "Not Set";
        let formattedTime = "Not Set";
        let customer_name = "Not Set";
        let branch = "Not Set";

        if (service_datetime !== "Not Set") {
            let dateObj = new Date(service_datetime);
            formattedDate = dateObj.toISOString().split("T")[0];
            formattedTime = dateObj.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        }

        if (frm.doc.reference_type == "Sales Order") {
            console.log("yes");
            frappe.model.with_doc(frm.doc.reference_type, frm.doc.reference_name, function() {
                let sales_order_doc = frappe.get_doc(frm.doc.reference_type, frm.doc.reference_name);
                customer_name = sales_order_doc.customer || "Not Set";
                branch = sales_order_doc.cost_center || "Not Set";
                updatePreview();
            });
        } else {
            updatePreview();
        }

        function updatePreview() {
            if (previewBlock.length === 0) {
                previewBlock = $(`
                <div style="display: flex; flex-direction: column; justify-content: start; align-items: start; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #fff;" class="preview-block form-layout">
                    <p><strong>Loading...</strong></p>
                </div>
                `);

                $(frm.wrapper).find('.std-form-layout').before(previewBlock);
            }

            let previewContent = `
                <h4>Task Overview</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                    <div style="flex: 1; min-width: 200px;">
                        <p><strong>Assigned To:</strong> Loading...</p>
                        <p><strong>Customer:</strong> ${customer_name}</p>
                        <p><strong>Branch:</strong> ${branch}</p>
                    </div>
                    <div style="flex: 1; min-width: 200px;">
                        <p><strong>Service Time:</strong> ${formattedTime}</p>
                        <p><strong>Service Date:</strong> ${formattedDate}</p>
                    </div>
                </div>
            `;

            if (allocated_to) {
                frappe.model.with_doc("User", allocated_to, function() {
                    let user_doc = frappe.get_doc("User", allocated_to);
                    let user_name = user_doc.full_name;

                    previewContent = `
                        <h4>Task Overview</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 300px;">
                            <div style="flex: 1; min-width: 200px;">
                                <p><strong>Assigned To:</strong> <a href="#">${user_name}</a></p>
                                <p><strong>Customer:</strong> ${customer_name}</p>
                                <p><strong>Branch:</strong> ${branch}</p>
                            </div>
                            <div style="flex: 1; min-width: 200px;">
                                <p><strong>Service Date:</strong> ${formattedDate}</p>
                                <p><strong>Service Time:</strong> ${formattedTime}</p>
                            </div>
                        </div>
                    `;
                    $('.preview-block').html(previewContent);
                });
            } else {
                $('.preview-block').html(previewContent);
            }
        }
    },
    setup: function(frm) {
        frm.set_df_property('date', 'hidden', 1);
    }
});
