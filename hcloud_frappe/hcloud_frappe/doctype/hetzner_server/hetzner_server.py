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
        d = self.get_valid_dict()
        client = get_hetzner_client()
        return client.servers.create(
            name=d.name,
            server_type=client.server_types.get_by_name(d.server_type),
            image=client.images.get_by_name(d.image),
            ssh_keys=[client.ssh_keys.get_by_name(d.ssh_key)] if d.ssh_key else None,
        )

    def load_from_db(self):
        client = get_hetzner_client()
        server = client.servers.get_by_name(self.name)

        if not server:
            frappe.throw("Server not found", frappe.DoesNotExistError)

        data = {
            "name": server.name,
            "image": server.image.name,
            "server_type": server.server_type.name,
            "id": server.id,
            "status": server.status.capitalize(),
            "public_ip": server.public_net.ipv4.ip,
            "data_center": server.datacenter.name,
            "city": server.datacenter.location.city,
            "country": server.datacenter.location.country,
            "creation": server.created,
            "disk": server.server_type.disk,
            "memory": server.server_type.memory,
            "cores": server.server_type.cores,
            "cpu_type": server.server_type.cpu_type,
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

        if args.get("as_list"):
            return [
                (s.name, s.image.name, s.server_type.name, s.id, s.status.capitalize())
                for s in servers
            ]

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

    def delete(self):
        self._server.delete()
