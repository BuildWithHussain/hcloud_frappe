import frappe

from hcloud import Client

# HETZNER_API_KEY
def get_hetzner_client():
	api_key = frappe.conf.get("HETZNER_API_KEY")
	return Client(token=api_key)