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
