function csrf() {
	return { "X-CSRFToken": getCookie("csrftoken") }
}

const pCard = ({ so_name, partner_id, pickup_date, return_date, pickup_time, user_id, no_waiting, no_done, priority }) =>
	`<div class="card pr${priority}">
		<p><span class="title">${so_name}&nbsp;${partner_id}</span></p>
		<p class="right">${pickup_time}</p>
		<p>${pickup_date} &mdash; ${return_date}</p>
		<p class="right">${user_id}</p>
		<p>${no_waiting} waiting picks, ${no_done} done picks</p>
	</div>`;

const rCard = ({ so_name, partner_id, return_date, origin, time }) =>
	`<div class="card r">
		<p><span class="title">${so_name}&nbsp;${partner_id}</span></p>
		<p class="right">${time}</p>
		<p>${return_date}</p>
		<p>${origin}</p>
	</div>`;
	
const dCard = ({ so_name, partner_id, scheduled_date, time, body, user_id }) =>
	`<div class="card d">
		<p><span class="title">${so_name}&nbsp;${partner_id}</span></p>
		<p>${scheduled_date}, ${time}</p>
		<p class="right">${user_id}</p>
		${body}
	</div>`

function ajax_call() {
	$.ajax({
		type: 'GET',
		url: '/ajax/',
		headers: 'csrf()',
		success: function (response) {
			response = JSON.parse(response);
			console.log(response.run_data);
			$('div.column').empty();
			// console.log("empty");
			for (const x of response.to_pick_data) {
				$("#to_pick").append([{
					so_name: x.origin, 
					partner_id: x.partner_id[1], 
					pickup_date: x.pickup_date, 
					return_date: x.return_date, 
					pickup_time: x.scheduled_date, 
					user_id: x.user_id[0].user_id[1].split(' ')[0], 
					no_waiting: x.waiting_picks, 
					no_done: x.done_picks,
					priority: x.priority
				}].map(pCard).join())
			};
			for (const x of response.delivery_data) {
				$("#packed").append([{
					so_name: x.origin, 
					partner_id: x.partner_id[1], 
					pickup_date: x.pickup_date, 
					return_date: x.return_date, 
					pickup_time: x.scheduled_date, 
					user_id: x.user_id[0].user_id[1].split(' ')[0], 
					no_waiting: x.waiting_picks, 
					no_done: x.done_picks,
					priority: x.priority
				}].map(pCard).join())
			};
			for (const x of response.return_data) {
				$("#returns").append([{
					so_name: x.group_id[1], 
					partner_id: x.partner_id[1],
					return_date: x.scheduled_date,
					time: x.time,
					origin: x.origin
				}].map(rCard).join())
			};
			for (const x of response.run_data) {
				$("#runs").append([{
					so_name: x.origin,
					partner_id: x.partner_id,
					user_id: x.user_id[1].split(' ')[0],
					time: x.time,
					scheduled_date: x.scheduled_date,
					body: x.note
				}].map(dCard).join())
			};
			setTimeout(ajax_call, 30000) 
		}
	})
}

ajax_call()