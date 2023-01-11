let socket;
let messageCount = 10;
let noConnectionStyle = 'background-color:red'; //height: 50px; width: 50px;
let hasConnectionStyle = 'background-color:green'; //height: 50px; width: 50px;
let lastConnectionStatusResponse = Date.now();

document.getElementById('CONNECTION_STATUS').style = noConnectionStyle;

setInterval(() => {
	sendStatus();
	if (lastConnectionStatusResponse < Date.now() - 5000) {
		document.getElementById('CONNECTION_STATUS').style = noConnectionStyle;
	}
}, 5000);

function startEx() {
	let timestamp = GenerateDateTimeFromTimestampDonjaCrta(Math.floor(Date.now()));
	fetch(`/api/files/start/${timestamp}`);

	socket.send('START{"command":"StartExperiment","arguments":[]}END');

	RefreshFileList();
}
function stopEx() {
	socket.send('START{"command":"StopExperiment","arguments":[]}END');

	RefreshFileList();
}
function sendStatus() {
	socket.send('START{"command":"STATUS","arguments":[]}END');

	RefreshFileList();
}

function GenerateDateTimeFromTimestamp(tm) {
	let timestamp = new Date(tm);
	let hours = timestamp.getHours();
	let minutes = '0' + timestamp.getMinutes();
	let seconds = '0' + timestamp.getSeconds();
	let timeFormat = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	return timeFormat;
}

function GenerateDateTimeFromTimestampDonjaCrta(tm) {
	let timestamp = new Date(tm);
	let hours = timestamp.getHours();
	let minutes = '0' + timestamp.getMinutes();
	let seconds = '0' + timestamp.getSeconds();
	let timeFormat = hours + '_' + minutes.substr(-2) + '_' + seconds.substr(-2);
	return timeFormat;
}

function processDataFromSensor(data) {
	// console.log("DATA")
	if (data['data'] == 'STATUS')
		document.getElementById('CONNECTION_STATUS').style = hasConnectionStyle;
	else {
		let tmpDataArray = data['data'].split(',').map((a) => parseInt(a));
		let timeFormat = GenerateDateTimeFromTimestamp(parseInt(data['timestamp']) * 1000);
		document.getElementById('DATA').innerText = timeFormat;
		UpdateGraphsFromData(tmpDataArray, timeFormat);
	}
}

initSocket();

function initSocket() {
	let s = new WebSocket('ws://localhost:31310/web');

	s.onopen = function (e) {};

	s.onmessage = function (event) {
		const response = JSON.parse(event.data);
		if ('data' in response) processDataFromSensor(response);
		lastConnectionStatusResponse = Date.now();
	};

	s.onclose = function (event) {
		setTimeout(() => {
			initSocket();
		}, 1000);
	};
	s.onerror = function (error) {
		socket.close();
	};

	socket = s;
}
