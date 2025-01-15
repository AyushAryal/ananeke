frappe.views.calendar["ToDo"] = {
	field_map: {
		start: "start_date_time",
		end: "end_date_time",
		id: "name",
		title: "description",
		allDay: 0,
		progress: "progress",
	},
	gantt: true,
	filters: [
		{
			fieldtype: "Link",
			fieldname: "reference_type",
			options: "Task",
			label: __("Task"),
		},
		{
			fieldtype: "Dynamic Link",
			fieldname: "reference_name",
			options: "reference_type",
			label: __("Task"),
		},
	],
	get_events_method: "frappe.desk.calendar.get_events",
};
