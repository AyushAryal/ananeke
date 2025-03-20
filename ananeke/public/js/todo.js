frappe.ui.form.on("ToDo", {
    refresh: function(frm) {
        let previewBlock = $('.preview-block');
        let allocated_to = frm.doc.allocated_to;
        let service_datetime = frm.doc.start_date_time || "Not Set";

        let formattedDate = "Not Set";
        let formattedTime = "Not Set";

        if (service_datetime !== "Not Set") {
            let dateObj = new Date(service_datetime);
            formattedDate = dateObj.toISOString().split("T")[0];
            formattedTime = dateObj.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        }

        if (previewBlock.length === 0) {
            previewBlock = $(`
            <div style="display: flex; flex-direction: column; justify-content: start; align-items: start; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background-color: #fff;" class="preview-block form-layout">
                <p><strong>Loading...</strong></p>
            </div>
            `);

            $(frm.wrapper).find('.std-form-layout').before(previewBlock);
        }

        $('.preview-block').html(`
            <h4>Task Overview</h4>
            <p><strong>Assigned To:</strong> Loading...</p>
            <p><strong>Service Date:</strong> ${formattedDate}</p>
            <p><strong>Service Time:</strong> ${formattedTime}</p>
        `);

        if (allocated_to) {
            frappe.model.with_doc("User", allocated_to, function() {
                let user_doc = frappe.get_doc("User", allocated_to);
                let user_name = user_doc.full_name;

                $('.preview-block').html(`
                    <h4>Task Overview</h4>
                    <p><strong>Assigned To</strong> <a href="#"}>${user_name}</a></p>
                    <p><strong>Service Date</strong> ${formattedDate}</p>
                    <p><strong>Service Time</strong> ${formattedTime}</p>
                `);
            });
        } else {
            $('.preview-block').html(`
                <h4>Task Overview</h4>
                <p><strong>Assigned To:</strong> Not Assigned</p>
                <p><strong>Service Date</strong> ${formattedDate}</p>
                <p><strong>Service Time</strong> ${formattedTime}</p>
            `);
        }
    },
    setup: function(frm) {
        frm.set_df_property('date', 'hidden', 1);
    }
});
