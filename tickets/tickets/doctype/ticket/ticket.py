# Copyright (c) 2026, workshop team and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Ticket(Document):
	def before_save(self):
		pass

	def validate(self):
		can_raise_ticket = frappe.get_value(
			"Employee", {"user_id": frappe.session.user}, "custom_can_raise_ticket"
		)
		if not can_raise_ticket:
			frappe.throw("You are not allowed to raise a ticket")
		
		open_tickets = frappe.db.count(
			"Ticket", {"owner": frappe.session.user, "workflow_state": "Open"}
		)
		if open_tickets >= 3 and self.workflow_state in ["Open", "Draft", "", None]:
			frappe.throw("You can not raise a ticket <br>You have 3 Open tickets")
