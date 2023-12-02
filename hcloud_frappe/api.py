import frappe

@frappe.whitelist()
def execute_action_on_server(name, action):
    VALID_ACTIONS = ["shutdown", "reboot", "power_on"]

    if action not in VALID_ACTIONS:
        frappe.throw("Invalid Action for Server")
    
    server = frappe.get_doc("Hetzner Server", name)
    getattr(server, action)()
