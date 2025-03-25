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

for(let toggle of toggles) {
	toggle.dataset.clicked = "0";
	toggle.addEventListener("click", function() {

		this.dataset.clicked = this.dataset.clicked === "1" ? "0" : "1";

		if(this.dataset.clicked === "0") {
			this.classList.remove("toggleClickedTrue");
		}
		else {
			this.classList.add("toggleClickedTrue");
		}
	})
}
