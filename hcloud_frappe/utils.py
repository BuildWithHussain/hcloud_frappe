import frappe

from hcloud import Client


# HETZNER_API_KEY
def get_hetzner_client():
    api_key = frappe.conf.get("HETZNER_API_KEYS")
    project_id = frappe.conf.get("HETZNER_PROJECT_ID")

    if not (api_key and project_id):
        frappe.throw(
            "Hetzner API Key and Project ID are required before creating a client object. Please place HETZNER_API_KEY and HETZNER_PROJECT_ID in site_config.json."
        )

    return Client(token=api_key)
