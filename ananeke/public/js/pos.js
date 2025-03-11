frappe.provide('erpnext.PointOfSale');
frappe.require('point-of-sale.bundle.js', function () {

    erpnext.PointOfSale.Controller = class MyPosController extends erpnext.PointOfSale.Controller {
        constructor(wrapper) {
            super(wrapper);
        }

        make_app() {
            super.make_app();
            this.prepare_get_items_btn();
        }

        prepare_get_items_btn() {

            this.page.page_actions.find(".custom-actions").empty();
        
            this.prepare_fullscreen_btn();
        
            this.page.add_button(__("Get Items"), null, { 
                btn_class: "btn btn-primary get-items-btn"
            });
        
            this.bind_get_items_events();
            this.bind_fullscreen_events();
        }

        bind_get_items_events() {
            this.$get_items_btn = this.page.page_actions.find(".get-items-btn");
        
            this.$get_items_btn.on("click", async () => {
                try {
                    if (!this.customer_details || Object.keys(this.customer_details).length === 0) {
                        frappe.msgprint("Select a Customer");
                        return;
                    }
        
                    let records = await frappe.db.get_list("Patient", {
                        filters: { customer: this.customer_details.customer },
                        fields: ["name"],
                        limit_page_length: 1
                    });
        
                    if (records.length === 0) {
                        console.log("No patient found for this customer.");
                        return;
                    }
        
                    let patient = records[0].name;
                    let args = { patient, customer: this.frm.doc.customer, company: this.frm.doc.company };
        
                    let response = await frappe.call({
                        method: 'healthcare.healthcare.utils.get_healthcare_services_to_invoice',
                        args: args
                    });
        
                    if (response.message) {
                        if (!Array.isArray(this.frm.doc.items)) {
                            this.frm.doc.items = [];
                        }
        
                        for (const obj of response.message) {
                            try {
                                let item = await frappe.db.get_doc("Item", obj.service);
                                console.log(item);
        
                                let existingItem = this.frm.doc.items.find(i => i.item_code === item.item_code);
        
                                if (!existingItem) {
                                    let pos_invoice_item = {
                                        docstatus: 0,
                                        doctype: "POS Invoice Item",
                                        item_code: item.item_code,
                                        item_name: item.item_name,
                                        warehouse: 'Stores - A',
                                        description: item.description,
                                        qty: 1,
                                        uom: item.stock_uom,
                                        rate: item.standard_rate || 0,
                                        amount: (item.standard_rate || 0) * 1,
                                        net_amount: (item.standard_rate || 0) * 1,
                                        parenttype: "POS Invoice",
                                    };
        
                                    console.log(pos_invoice_item);
        
                                    this.frm.doc.items.push(pos_invoice_item);
                                    await this.frm.save();
                                } else {
                                    console.log(existingItem);
                                    console.log(`Item ${item.item_code} already exists in the invoice.`);
                                }
                            } catch (error) {
                                console.error("Error fetching item:", error);
                            }
                        }
                    } else {
                        console.log("No message received.");
                    }
                } catch (err) {
                    console.error("Error:", err);
                }
            });
        }
        
        
        
        prepare_fullscreen_btn() {
            this.page.page_actions.find(".custom-actions").empty();
            this.page.add_button(__("Full Screen"), null, { btn_class: "btn-default fullscreen-btn" });
            this.bind_fullscreen_events();
        }
    };

    wrapper.pos = new erpnext.PointOfSale.Controller(wrapper);
    window.cur_pos = wrapper.pos;
});
