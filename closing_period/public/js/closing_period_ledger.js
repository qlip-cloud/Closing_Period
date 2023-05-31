frappe.ui.form.on('Period Closing Voucher', {
	
	refresh: function(frm) {
		if(frm.doc.docstatus > 0) {
			frm.add_custom_button(__('Ledger'), function() {
                if (!frm.doc.qp_finance_book) {
					frappe.route_options = {
                        "voucher_no": frm.doc.name,
                        "from_date": frm.doc.posting_date,
                        "to_date": moment(frm.doc.modified).format('YYYY-MM-DD'),
                        "company": frm.doc.company,
                        "group_by": "",
                        "show_cancelled_entries": frm.doc.docstatus === 2
                    };
                    frappe.set_route("query-report", "General Ledger");
				}
                else {
                    console.log(!frm.doc.qp_finance_book)
                    frappe.route_options = {
                        "voucher_no": frm.doc.name,
                        "finance_book": frm.doc.qp_finance_book,
                        "include_default_book_entries": !frm.doc.qp_finance_book,
                        "from_date": frm.doc.posting_date,
                        "to_date": moment(frm.doc.modified).format('YYYY-MM-DD'),
                        "company": frm.doc.company,
                        "group_by": "",
                        "show_cancelled_entries": frm.doc.docstatus === 2
                    };
                    frappe.set_route("query-report", "General Ledger");
                }
				
			}, "fa fa-table");
		}
	}

})
