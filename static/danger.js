function showDangerMessage(value) {
	var dangerInfo = document.getElementById("dangerInfo");
	if( value>= 27){
		dangerInfo.style.display = "block";
	}
	else {
                dangerInfo.style.display = "none";
	}
}
