import frappe


def sales_order(doc, method):
    if method == "before_save":
        # if doc.service_date_time:
        #     doc.delivery_date = doc.service_date_time.split(" ")[0]
        ...