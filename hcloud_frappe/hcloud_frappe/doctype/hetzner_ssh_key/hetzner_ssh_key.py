# Copyright (c) 2023, Build With Hussain and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
from hcloud_frappe.utils import get_hetzner_client


class HetznerSSHKey(Document):
	def db_insert(self, *args, **kwargs):
		client = get_hetzner_client()
		return client.ssh_keys.create(
			name=self.name,
			public_key=self.public_key
		)

	def load_from_db(self):
		client = get_hetzner_client()
		key = client.ssh_keys.get_by_name(self.name)
		self._key = key

		data = {
			"name": key.name,
			"public_key": key.public_key,
			"fingerprint": key.fingerprint,
			"labels": key.labels,
			"id": key.id,
			"created": key.created,
		}
		super(Document, self).__init__(frappe._dict(data))

	def db_update(self):
		pass

	@staticmethod
	def get_list(args):
		client = get_hetzner_client()
		keys = client.ssh_keys.get_all()

		if args.get("as_list"):
			return [(key.name, key.public_key, key.fingerprint) for key in keys]
		
		return [
			{
				"name": key.name,
				"public_key": key.public_key,
				"fingerprint": key.fingerprint,
				"labels": key.labels,
				"id": key.id,
				"created": key.created,
			}
			for key in keys
		]

	@staticmethod
	def get_count(args):
		pass

	@staticmethod
	def get_stats(args):
		pass

	def delete(self):
		self._key.delete()
