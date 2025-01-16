from frappe.model.meta import get_meta

def custom_get_list_view_fields(doctype):
    meta = get_meta(doctype)
    return [field for field in meta.get_list_view_fields() if field.fieldname != "due_date"]
