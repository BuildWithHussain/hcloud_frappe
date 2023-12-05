# Copyright (c) 2023, Build With Hussain and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

from hcloud_frappe.utils import get_hetzner_client


class HetznerServerImage(Document):
	
	def db_insert(self, *args, **kwargs):
		pass

	def load_from_db(self):
		client = get_hetzner_client()
		image = client.images.get_by_name(self.name)
		data = frappe._dict({
			"name": image.name,
			"os_flavor": image.os_flavor,
			"os_version": image.os_version,
			"status": image.status.capitalize(),
			"description": image.description,
		})

		self._image = image
		super(Document, self).__init__(data)

	def db_update(self):
		pass

	@staticmethod
	def get_list(args):
		client = get_hetzner_client()
		images = client.images.get_all()

		if args.get("as_list"):
			return [(image.name,image.description,image.description) for image in images]
		
		return [frappe._dict({
			"name": image.name,
			"os_flavor": image.os_flavor,
			"os_version": image.os_version,
			"status": image.status.capitalize(),
			"description": image.description,
		}) for image in images]

	@staticmethod
	def get_count(args):
		pass

	@staticmethod
	def get_stats(args):
		pass

