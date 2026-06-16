frappe.ready(function () {
	// bind events here
	frappe.web_form.on("subject", () => {
		frappe.msgprint("hello files")
	});
})