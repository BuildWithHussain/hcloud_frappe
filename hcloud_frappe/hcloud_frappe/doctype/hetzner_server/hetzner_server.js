// Copyright (c) 2023, Build With Hussain and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hetzner Server", {
  refresh(frm) {
	frm.add_web_link(
		`https://console.hetzner.cloud/projects/${frm.doc.project_id}/servers/${frm.doc.id}/overview`, 
		"View in Hetzner Console"
	);

	const action_label_map = {
		"shutdown": "Shutdown",
		"power_on": "Power On",
		"reboot": "Reboot",
	}

	for (const action in action_label_map) {
		frm.add_custom_button(__(action_label_map[action]), () => {
			frappe
          .xcall(`hcloud_frappe.api.execute_action_on_server`, {
            name: frm.doc.name,
			action: action
          })
          .then((r) => {
            frappe.show_alert(__(`${action_label_map[action]} triggered`));
            // frm.reload_doc();
          });
		}, "Actions")
	}
  },
});
