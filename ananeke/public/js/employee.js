frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        let commissionBlock = $('.commission-block');

        if (commissionBlock.length === 0) {
            commissionBlock = `
            <div class="commission-block">
                <h3>Employee Commission</h3>
                <p>Commission Accumulated: <strong id="commission-balance">Loading...</strong></p>
            </div>
            `;
            
            $(frm.wrapper).find('.layout-main-section').prepend(commissionBlock);
        }

        frappe.call({
            method: 'ananeke.methods.employee.employee_accumulated_commission',
            args: {
                employee_id: frm.doc.name
            },
            callback: function(response) {
                const data = response.message;

                if (data && data.accumulated_commission !== undefined) {
                    const commission = parseFloat(data.accumulated_commission).toFixed(2);
                    $('#commission-balance').text(commission);
                } else {
                    $('#commission-balance').text('N/A');
                }
            }
        });
    }
});
