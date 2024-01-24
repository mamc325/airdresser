var currentTemperature;
var currentHumidity;

// 현재 온도 업데이트 함수
function updateTemperature(value) {
    currentTemperature = parseInt(value, 10);
}

// 현재 습도 업데이트 함수
function updateHumidity(value) {
    currentHumidity = parseInt(value, 10);
}

function showWeather() {
    var weatherInfoElement = document.getElementById("weatherInfo");
    var rainInfo= document.getElementById("rainInfo");

    weatherInfoElement.innerHTML = '현재 온도와 습도는 ' + currentTemperature + '°C, ' + currentHumidity + '%입니다.';
    var weatherImageElement = document.getElementById("weather-image");
    rainInfo.style.display = "block";
    if (currentHumidity > 70) {
        weatherImageElement.src = "/static/rain.jpg"; // 높은 습도 이미지
    }
    else
        weatherImageElement.src = "/static/sunny.jpg"; // 화창한 이미지 
}


