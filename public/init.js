let pressCipher = document.getElementById('pressCipher');
let pressCaesar = document.getElementById('pressCaesar');
let pressAlgebraic = document.getElementById('pressAlgebraic');
let pressPoint = document.getElementById('pressPoint');
let pressPlace = document.getElementById('pressPlace');
let pressSymbol = document.getElementById('pressSymbol');

pressCipher.onclick = () => window.location.href = "./front.html";
pressCaesar.onclick = () => window.location.href = "./caesar.html";
pressAlgebraic.onclick = () => window.location.href = "./algebraic.html";
pressPoint.onclick = () => window.location.href = "./point.html";
pressPlace.onclick = () => window.location.href = "./place.html";
pressSymbol.onclick = () => window.location.href = "./symbol.html";

let toggles = document.querySelectorAll('toggle');

const changeEvent = new Event("change");

for(let toggle of toggles) {

	toggle.dataset.clicked = toggle.dataset.clicked === "1" ? "0" : "1";

	function click() {
		this.dataset.clicked = this.dataset.clicked === "1" ? "0" : "1";

		if(this.dataset.clicked === "0") {
			this.classList.remove("toggleClickedTrue");
		}
		else {
			this.classList.add("toggleClickedTrue");
		}

		this.dispatchEvent(changeEvent);
	}

	click.bind(toggle)();

	toggle.addEventListener("click", click)
}

function download(data, filename, type) {
    var file = new Blob([data], {type: type});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        var a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        }, 0);
    }
}

function setSaveCipher(fetcher) {

	preview = function() {
		if(document.getElementById("preview").dataset.clicked === "1") {
			fetcher().then(text => document.getElementById("showPreview").textContent = text).catch(() => document.getElementById("showPreview").textContent = "No preview available, settings may not be set up or correct.");
		}
	}

	saveResultClip.addEventListener('click',() => {
		fetcher().then(text => navigator.clipboard.writeText(text));
	})

	saveResultTxt.addEventListener('click',() => {
		fetcher().then(text => download(text,"cipher.txt","text/plain"));
	})

	let previewInputs = document.querySelectorAll("#cipherFrom, #key, #decipher, #preview, #rangeLower, #rangeUpper, #alphabet"); //Change event
	for (let input of previewInputs) {
		input.addEventListener("change", preview);
	}
	previewInputs = document.querySelectorAll("#cipherFrom, #key, #rangeLower, #rangeUpper, #alphabet"); //key pressing event
	for (let input of previewInputs) {
		input.addEventListener("keydown", () => setTimeout(preview,0));
	}
	// for (let input of previewInputs) {
	// 	input.addEventListener("keyup", preview);
	// }
}

try {
	let importClip = document.getElementById("importClip");
	let importText = document.getElementById("importText");
	let importTextRepresent = document.getElementById("importTextRepresent");

	if (!importClip || !importText || !importTextRepresent) throw new Error();

	importClip.addEventListener("click", () => {
		navigator.clipboard.readText().then((text) => {
			document.getElementById("cipherFrom").value = text;
		});
	});

	importText.addEventListener("change", function() {
		let files = this.files;
		if (!files || files.length !== 1) return;
		let file = files[0];
		file.text().then(text => document.getElementById("cipherFrom").value = text);
	});

	importTextRepresent.addEventListener("click", (event) => {
		document.getElementById("importText").click();
	})
}
catch{}

function make( type = "div", options = {}, appendTo = document.body) {
	if (!type) throw new Error(`'Make' type is falsy (${type}).`);
	if (!appendTo) appendTo = document.body;
	else {
		if (typeof appendTo === "string") {
		    appendTo = document.getElementById(appendTo);
		    if (!appendTo)
		    throw new Error(
		        `"make": Element from input ID (${appendTo}) not found!`,
		    );
		}
	}
    let dataset = {};
    if (options.dataset) {
        dataset = options.dataset;
        delete options.dataset
    }
    let style = {};
    if (options.style) {
        style = options.style;
        delete options.style;
    }
	let HTMLobj = Object.assign(
		appendTo.appendChild(document.createElement(type)),
		options,
	);
	Object.assign(HTMLobj.style, style);
	Object.assign(HTMLobj.dataset, dataset);
	return HTMLobj;
}

const cipherList = document.getElementById("cipherList");

// class HTMLExtension {

// 	static idList = [];

// 	static get(element) {
// 		let found = HTMLExtension.idList.filter(e => e.element === element);
// 		if (found) return found[0]
// 		else return null;
// 	}
// 	constructor(htmlObject) {
// 		this.element = htmlObject;
// 		this.custom = {};
// 		HTMLExtension.idList.push(this);
// 	}
// }

function saveLocalData(data) {
	let presets = JSON.parse(localStorage.getItem("stored_cipher_presets") || "[]");

	presets.push(data);

	localStorage.setItem("stored_cipher_presets", JSON.stringify(presets));
}

function removeLocalData(index) {
	let presets = JSON.parse(localStorage.getItem("stored_cipher_presets") || "[]");

	presets.splice(index, 1);

	localStorage.setItem("stored_cipher_presets", JSON.stringify(presets));
}

function getLocalData(index) {
	let presets = JSON.parse(localStorage.getItem("stored_cipher_presets") || "[]");

	return presets[index];
}

function getAllLocalData() {
	let presets = JSON.parse(localStorage.getItem("stored_cipher_presets") || "[]");
	return presets;
}

function updateCipherList() {
	cipherList.innerHTML = "";

	json = getAllLocalData();
	for(let index in json) {
		let per = json[index];

		let holder = make('div', {className: "cipherListEntry"}, cipherList);

		let button = make("button", {
			className: "cipherListEntryButton",
			innerHTML: per.name,
			dataset: {
				type: per.type,
				id: index
			}
		}, holder);
		let remove = make("button", {
			className: "cipherListEntryButton xButton",
			innerHTML: "x",
			dataset: {
				id: index
			}
		}, button);
		button.addEventListener('click', function() {
			window.location.href = this.dataset.type + ".html?preset=" + this.dataset.id;
		});
		remove.addEventListener('click', function(event) {

			event.stopPropagation();

			if (!confirm("Are you sure you want to remove cipher preset " + per.name + "?")) return;

			removeLocalData(parseInt(this.dataset.id));

			updateCipherList()

			// fetch('/cookie_save', {
			// 	method: "POST",
			// 	body: JSON.stringify({
			// 		remove: this.dataset.id
			// 	})
			// }).then(() => updateCipherList());
		});
	}

}

updateCipherList();

let urlDissect = new URL(window.location.href).searchParams.get('preset');
if (urlDissect) urlDissect = parseInt(urlDissect);
