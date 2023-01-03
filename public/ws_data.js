HtmlCharts = document.getElementsByClassName('Chart');

let NUM_OF_CHARTS = 6;
let COLOR_OF_CHARTS = ['#49be25', '#f22e02', '#0286f2', '#f2da02', '#f202ce', '#02eef2'];
let Charts = [];
let MAX_CHART_LABELS_LEN = 100;

for (let c = 0; c < HtmlCharts.length; c++) {
	var ctx = HtmlCharts[c].getContext('2d');
	var lineChart = new Chart(ctx, {
		type: 'line',
		options: {
			animation: true,
			responsive: true,
			maintainAspectRatio: false,
		},
		data: {
			labels: [],
			datasets: [
				{
					label: `Senzor ${c + 1}`,
					data: [],
					borderColor: COLOR_OF_CHARTS[c],
				},
			],
		},
	});

	Charts.push(lineChart);
}

let UpdateDataCallback = [];
function GenerateUpdateDataCallback(chart) {
	return (data, label) => {
		chart.data.labels.push(label);
		chart.data.datasets[0].data.push(data);

		if (chart.data.datasets[0].data.length > MAX_CHART_LABELS_LEN)
			chart.data.datasets[0].data.shift();
		if (chart.data.labels.length > MAX_CHART_LABELS_LEN) chart.data.labels.shift();

		chart.update();
	};
}

for (let c = 0; c < Charts.length; c++) {
	let chartCallback = GenerateUpdateDataCallback(Charts[c]);
	UpdateDataCallback.push(chartCallback);
}

var ctx = document.getElementById('line-chart').getContext('2d');
var fullChart = new Chart(ctx, {
	type: 'line',
	options: {
		responsive: true,
		animation: true,
		maintainAspectRatio: false,
	},
	data: {
		labels: [],
		datasets: Array.from(Array(NUM_OF_CHARTS).keys()).map((idx) => {
			return {
				label: `Senzor ${idx + 1}`,
				data: [],
				borderColor: COLOR_OF_CHARTS[idx],
			};
		}),
	},
});

function UpdateGraphsFromData(dataArray, label) {
	fullChart.data.labels.push(label);
	if (fullChart.data.labels.length > MAX_CHART_LABELS_LEN) fullChart.data.labels.shift();

	for (let c = 0; c < UpdateDataCallback.length; c++) {
		UpdateDataCallback[c](dataArray[c], label);
		fullChart.data.datasets[c].data.push(dataArray[c]);
		if (fullChart.data.datasets[c].data.length > MAX_CHART_LABELS_LEN)
			fullChart.data.datasets[c].data.shift();
	}

	fullChart.update();
}
