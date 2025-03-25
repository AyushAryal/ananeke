frappe.ui.form.on('Employee Target', {
    refresh: function (frm) {
        compute_progress(frm);
    },
    achieved: function (frm) {
        compute_progress(frm);
    },
    target: function (frm) {
        compute_progress(frm);
    }
});

function compute_progress(frm) {
    if (frm.doc.target && frm.doc.achieved) {
        frm.set_value('progress', (frm.doc.achieved / frm.doc.target) * 100);
    } else {
        frm.set_value('progress', 0);
    }
    frm.save();
}
