# Copyright (c) 2023, Build With Hussain and contributors
# For license information, please see license.txt
import frappe

from hcloud_frappe.utils import get_hetzner_client


def execute(filters=None):
	columns = [
		{"fieldtype": "Data", "fieldname": "usage", "label": "Usage"},
		{"fieldtype": "Float", "fieldname": "timestamp", "label": "Timestamp"},
	]

	data = get_metrics_from_hetzner(filters)
	chart = {
		"data": {
			"labels": [row["timestamp"] for row in data],
			"datasets": [
				{
					"name": "Usage",
					"values": [row["usage"] for row in data],
					"chartType": "line",
				}
			],
		},
		"type": "line",
	}

	return columns, data, None, chart


def get_metrics_from_hetzner(filters):
	import datetime
	client = get_hetzner_client()

	server_name = filters.get("server_name")
	metric_type = filters.get("metric_type")

	server_id = frappe.get_doc("Hetzner Server", server_name).id

	response = client.request(
		"GET",
		f"/servers/{server_id}/metrics?type={metric_type}&start=2023-12-09T13:14:18.316Z&end=2023-12-09T13:19:18.316Z",
	)

	key = "cpu"
	if metric_type == "disk":
		key = "disk.0.bandwidth.write"

	if metric_type == "network":
		key = "network.0.bandwidth.in"

	values = response["metrics"]["time_series"][key]["values"]
	data = []
	# process the response
	for timestamp, value in values:
		data.append({"timestamp": timestamp, "usage": value})
	
	# timestamp is in utc seconds format
	# convert it to ISO
	for row in data:
		row["timestamp"] = datetime.datetime.fromtimestamp(row["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

	return data
