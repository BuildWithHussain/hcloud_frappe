# Copyright (c) 2023, Build With Hussain and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from hcloud_frappe.utils import get_hetzner_client

# running
# initializing
# starting
# stopping
# off
# deleting
# migrating
# rebuilding
# unknown


class HetznerServer(Document):
	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		client = get_hetzner_client()
		server = client.servers.get_by_name(self.name)
		data = {
			"name": server.name,
			"image": server.image.name,
			"server_type": server.server_type.name,
			"id": server.id,
			"status": server.status.capitalize(),
		}

		self._server = server
		super(Document, self).__init__(frappe._dict(data))

	def shutdown(self):
		self._server.shutdown()
	
	def power_on(self):
		self._server.power_on()
	
	def reboot(self):
		self._server.reboot()


	def db_update(self):
		pass

	@staticmethod
	def get_list(args):
		client = get_hetzner_client()
		servers = client.servers.get_all()


		return [
			frappe._dict(
				{
					"name": s.name,
					"image": s.image.name,
					"server_type": s.server_type.name,
					"id": s.id,
					"status": s.status.capitalize(),
				}
			)
			for s in servers
		]

	@staticmethod
	def get_count(args):
		pass

	@staticmethod
	def get_stats(args):
		pass
