# Copyright (c) 2023, Build With Hussain and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document

from hcloud_frappe.utils import get_hetzner_client


class HetznerServerType(Document):
	
	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		client = get_hetzner_client()
		st = client.server_types.get_by_name(self.name)
		
		data = frappe._dict({
			"name": st.name,
			"disk": st.disk,
			"memory": st.memory,
			"cores": st.cores,
			"cpu_type": st.cpu_type,
			"description": st.description,
		})

		self._server_type = st
		super(Document, self).__init__(data)

	def db_update(self):
		pass

	@staticmethod
	def get_list(args):
		client = get_hetzner_client()
		server_types = client.server_types.get_all()
		return [frappe._dict({
			"name": st.name,
			"disk": st.disk,
			"memory": st.memory,
			"cores": st.cores,
			"cpu_type": st.cpu_type,
			"description": st.description,
		}) for st in server_types]

	@staticmethod
	def get_count(args):
		pass

	@staticmethod
	def get_stats(args):
		pass

