frappe.listview_settings["ToDo"] = {
    add_fields: ["status", "priority"],

    onload: function (listview) {
        listview.page.fields_dict.date.$wrapper.hide();
        // listview.fields = listview.fields.filter(field => !field.includes("date"));
        listview.fields = listview.fields.filter(field => field[0] !== "date");
        // listview.render()
    }
};
