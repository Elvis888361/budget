// Copyright (c) 2024, aqiq Budget and contributors
// For license information, please see license.txt
frappe.provide("erpnext.accounts.dimensions");
frappe.ui.form.on("Monthly Budget Distribution Tool", {
	refresh(frm) {
        frm.set_query("cost_center", function() {
			return {
				filters: {
					company: frm.doc.company
				}
			};
		});
        erpnext.accounts.dimensions.setup_dimension_filters(frm, frm.doctype);
	},
});
