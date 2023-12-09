// Copyright (c) 2023, Build With Hussain and contributors
// For license information, please see license.txt

frappe.query_reports["Hetzner Server Metrics"] = {
	"filters": [
		{
			"fieldname": "server_name",
			"label": "Server",
			"fieldtype": "Link",
			"options": "Hetzner Server",
			"reqd": 1
		},
		{
			"fieldname": "metric_type",
			"label": "Metric Type",
			"fieldtype": "Select",
			"options": "cpu\ndisk\nnetwork",
			"reqd": 1,
			"default": "cpu"
		}
	]
};
