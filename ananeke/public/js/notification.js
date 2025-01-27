// frappe.ready(function() {
//     frappe.realtime.on('notification', function(data) {
//         console.log('Real-time Notification Received:', data);

//         let message = data.message; 
//         let taskUrl = data.task_url; // The link to the task
//         let user = data.user; // The user for whom the notification is intended

//         frappe.notifications.add({
//             title: data.event,  // For example, "New Task Assigned"
//             message: message,  // The notification message
//             link: taskUrl,  // The link to the task
//             type: 'info'  // The type of notification (info, warning, etc.)
//         });
//     });
// });

// frappe.ready(function() {
//     var footer = $("footer");
//     if (footer.length > 0) {
//         footer.html(`
//             <div style="text-align: center; padding: 10px; background-color: #f8f8f8; color: #333;">
//                 <p>&copy; 2025 My Custom ERP. All Rights Reserved.</p>
//                 <p>Powered by <a href="https://www.mycompany.com" target="_blank">My Company</a></p>
//             </div>
//         `);
//     } else {
//         console.log("Footer element not found.");
//     }
// });