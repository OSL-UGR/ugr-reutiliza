const input = document.querySelector("#foto");
const preview = document.querySelector(".preview");
const aniadir = document.querySelector(".aniadir");
const form = document.querySelector(".addMueble");

async function createFileFromURL(url, filename) {
	try {
		// Fetch the file
		const response = await fetch(url);
		const blob = await response.blob();

		// Create a new File object
		const file = new File([blob], filename, { type: blob.type });

		return file;
	} catch (error) {
		console.error('Error creating file from URL:', error);
		throw error;
	}
}

let filesData = [];
async function fillFiles() {
	for (let foto of {{fotos|safe}}){
		let name = foto.substring(foto.lastIndexOf('/') + 1);

		try {
			const file = await createFileFromURL(foto, name);
			filesData.push(file);
		} catch (error) {
			console.error('Error processing URL:', foro, error);
		}
	}
	updateImageDisplay();
};
fillFiles();



form.addEventListener('submit', function(event) {
	event.preventDefault();
	sendData();
});

async function sendData() {
	if(filesData.length === 0){
		console.error('Formulario vacío detectado');
	}
	else{
		const picForm = new FormData(form);

		Array.from(filesData).forEach(file => {
			picForm.append('files', file);
		});

		const response = await fetch('{{action}}', {
			method: 'POST',
			body: picForm,
		});

		const redirectURL = response.url;
		window.location.href = redirectURL;
	}
}

aniadir.addEventListener('click', triggerForm);

function triggerForm() {
	input.click();
}

function updateImageDisplay() {

	let curFiles = [];

	curFiles = input.files;
	for(const file of curFiles) {
		!filesData.some((innerFile) => innerFile.name === file.name) 
			&& validFileType(file) && filesData.push(file);
	}
	drawImages();
}

function drawImages(){
	while (preview.firstChild) {
		preview.removeChild(preview.firstChild);
	}
	for (const file of filesData) {
		let image = document.createElement("img");
		let cross = document.createElement("div");
		let div = document.createElement("div");

		try{
			image.src = URL.createObjectURL(file);
		} catch{
			image.src = file;
		}
		image.alt = image.title = file.name;
		image.style.margin = '1em';
		image.classList.add('image');
		div.appendChild(image);

		cross.classList.add('cross-overlay');			
		cross.textContent = 'X';

		cross.addEventListener('click', function() {
			var index = filesData.findIndex((innerFile) => innerFile.name === image.title);

			filesData.splice(index,1);
			image.parentNode.remove();
			input.value = '';
		});

		div.appendChild(cross);
		div.classList.add('div-img');
		preview.appendChild(div);
	}
	preview.appendChild(aniadir);

}

const fileTypes = [
	"image/apng",
	"image/bmp",
	"image/gif",
	"image/jpg",
	"image/jpeg",
	"image/pjpeg",
	"image/png",
	"image/svg+xml",
	"image/tiff",
	"image/webp",
	"image/x-icon",
];

function validFileType(file) {
	return fileTypes.includes(file.type);
}

function returnFileSize(number) {
	if (number < 1024) {
		return `${number} bytes`;
	} else if (number >= 1024 && number < 1048576) {
		return `${(number / 1024).toFixed(1)} KB`;
	} else if (number >= 1048576) {
		return `${(number / 1048576).toFixed(1)} MB`;
	}
}

