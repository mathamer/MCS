function RefreshFileList() {
	fetch('/api/files/list')
		.then((response) => response.json())
		.then((data) => {
			let fileListElement = document.getElementById('FileList');
			fileListElement.innerHTML = '';

			data.map((filename) => {
				fileListElement.appendChild(GenerateFileListChild(filename));
			});
		});
}

function GenerateFileListChild(filename) {
	let listItem = document.createElement('li');
	let child = document.createElement('button');
	let analyze = document.createElement('button');
	let remove = document.createElement('button');
	let link = document.createElement('a');

	link.setAttribute('href', `/api/files/${filename}`);
	link.innerHTML = filename;

	child.appendChild(link);
	child.setAttribute('class', 'BUTTON_START SpaceingSmall');

	analyze.setAttribute('onclick', `AnalyzeFilename("${filename}")`);
	analyze.innerHTML = 'Analiza';
	analyze.setAttribute('class', 'BUTTON_OPTION SpaceingSmall');

	remove.setAttribute('onclick', `RemoveFilename("${filename}")`);
	remove.innerHTML = 'Del';
	remove.setAttribute('class', 'BUTTON_REMOVE SpaceingSmall');

	listItem.appendChild(child);
	listItem.appendChild(analyze);
	listItem.appendChild(remove);
	return listItem;
}

function AnalyzeFilename(filename) {
	window.open(`http://localhost:8050?filename=${filename}`);
}

function RemoveFilename(filename) {
	fetch(`/api/files/${filename}/remove`);
	RefreshFileList();
}

RefreshFileList();
