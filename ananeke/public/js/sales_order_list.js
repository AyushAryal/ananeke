// frappe.listview_settings["Sales Order"] = {
//     onload: function (listview) {
//         const customer_field = listview.page.fields_dict.customer;
        
//         listview.page.add_field({
//             label: __("Cost Center"),
//             fieldtype: "Link",
//             options: "Cost Center",
//             fieldname: "cost_center",
//             onchange: function () {
//                 const cost_center = listview.page.fields_dict.cost_center.get_value();
//                 listview.filter_area.add({
//                     fieldname: "cost_center",
//                     fieldtype: "Link",
//                     options: "Cost Center",
//                     operator: "=",
//                     value: cost_center,
//                 });
//             },
//         });

//         const cost_center_field = listview.page.fields_dict.cost_center.$wrapper;
//         cost_center_field.insertAfter(customer_field.$wrapper);
//     },
// };

frappe.listview_settings['Sales Order'] = {
    hide_name_column: true,

    onload: function(listview) {

        console.log(listview.$result);
        
        // listview.$result.findAll('.list-row-container').each(function() {
        //     let row = $(this);
        //     let docname = row.attr("data-name");
        //     console.log(row);


        //     if (docname) {

        //         frappe.db.get_value('Sales Order', docname, 'seen').then(r => {
        //             if (r.message && r.message.seen !== undefined) {
        //                 if (r.message.seen === 0 || r.message.seen === null) {
        //                     row.css("background", "#ffebeb");  // Light red for unopened
        //                 } else {
        //                     row.css("background", "#e6ffe6");  // Light green for opened
        //                 }
        //             }
        //         });
        //     }
        // });
    }
};







