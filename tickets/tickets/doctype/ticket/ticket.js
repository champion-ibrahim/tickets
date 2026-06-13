// Copyright (c) 2026, workshop team and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ticket', {
	before_load: async function (frm) {
		const crt_res = await frappe.db.get_value(
			'Employee',
			{ "user_id": frappe.session.user },
			"custom_can_raise_ticket"
		)
		const can_raise_ticket = crt_res.message.custom_can_raise_ticket

		if (!can_raise_ticket) {
			frm.disable_save()
			frm.set_intro("You are not allowed to raise tickets, contact with HR.", 'orange')
		} else {
			frm.enable_save()
		}
	},
	refresh: function (frm) {

		frm.set_query('assigned_to', () => {
			return {
				"filters": {
					"role": "IT Support",
					"enabled": 1
				}
			}
		})
	}
});
