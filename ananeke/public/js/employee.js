frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        let commissionBlock = $('.commission-block');

        if (commissionBlock.length === 0) {
            commissionBlock = `
            <div style="display: flex; justify-content: center; align-items: center; padding-top: 10px; padding-bottom: 10px;" class="commission-block">
                <p><h5>Accumulated Commission</h5> Rs.<strong id="commission-balance">Loading...</strong></p>
            </div>
            `;
            
            $(frm.wrapper).find('.form-assignments').prepend(commissionBlock);
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
