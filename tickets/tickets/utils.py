import frappe
# from frappe.model.workflow import apply_workflow

def new_employee_ticket(doc, method=None):
    ticket = frappe.get_doc(
        {
            "doctype": "Ticket",
            "subject": f"Set up email and software environment for employee {doc.first_name}",
            "issue_type": "Software",
            "description": "Set up email, basic apps, and software environment",
        }
    )
    ticket.flags.ignore_validate = True
    ticket.insert(ignore_permissions=True)
    # apply_workflow(ticket, "Open")
    