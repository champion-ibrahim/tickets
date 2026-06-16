# Copyright (c) 2026, workshop team and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase



def create_test_employee():
	test_user_email = "test_employee@t.t"
	if not frappe.db.exists("User", test_user_email):
		user = frappe.get_doc({
			"doctype": "User",
			"email": test_user_email,
			"first_name": "Test",
			"last_name": "Employee",
			"send_welcome_email": 0
		})
		user.insert(ignore_permissions=True)

	employee_id = frappe.db.get_value("Employee", {"user_id": test_user_email}, "name")
	
	if employee_id:
		employee = frappe.get_doc("Employee", employee_id)
	else:
		employee = frappe.get_doc({
			"doctype": "Employee",
			"first_name": "Test Employee",
			"user_id": test_user_email,
			"gender": "Male",
			"date_of_joining": frappe.utils.today(),
			"date_of_birth": "1995-01-01"
		})
		
	employee.custom_can_raise_ticket = 1
	employee.save(ignore_permissions=True)
	return employee



class TestTicket(FrappeTestCase):
	
	def setUp(self):
		self.employee = create_test_employee()
		return super().setUp()

	def test_only_raise_three_tickets(self):
		frappe.set_user(self.employee.user_id)

		for i in range(3):
			ticket = frappe.get_doc({
				"doctype": "Ticket",
				"subject": f"Test Ticket {i+1}",
				"description": "Testing the ticket limit constraint.",
			})
			ticket.insert()

		fourth_ticket = frappe.get_doc({
			"doctype": "Ticket",
			"subject": "Test Ticket 4 (Should Fail)",
			"description": "This ticket should not be allowed.",
		})

		with self.assertRaises(frappe.ValidationError):
			fourth_ticket.insert()
