let ctx = null;
let chart = null;
let config = {
	// type은 차트 종류 지정
	type: 'line', // 라인그래프
	// data는 차트에 출력될 전체 데이터 표현
	data: {
		// labels는 배열로 데이터의 레이블들
		labels: [],
		// datasets 배열로 이 차트에 그려질 모든 데이터 셋 표현. 그래프 1개만 있음
		datasets: [
		{
			label: 'temp 센서로부터 측정된 실시간 온도',
			backgroundColor: 'green',
			borderColor: 'rgb(130, 99, 130)',
			borderWidth: 2,
			data: [], // 각 레이블에 해당하는 데이터
			fill : false, // 채우지 않고 그리기
		},
		{
			label: 'temp 센서로부터 측정된 실시간 습도',
			backgroundColor: 'blue',
			borderColor: 'rgb(255, 99, 132)',
			borderWidth: 2,
			data: [], // 각 레이블에 해당하는 데이터
			fill : false, // 채우지 않고 그리기
		},
		]
	},
	// 차트의 속성 지정
	options: {
		responsive : false, // 크기 조절 금지
		scales: { // x축과 y축 정보
			xAxes: [{
				display: true,
				scaleLabel: { display: true, labelString: '시간(0.1초)'},
			}],
			yAxes: [{
				display: true,
				scaleLabel: { display: true, labelString: '온도(c), 습도(%)' }
			}]
		}
	}
};
let LABEL_SIZE = 20; // 차트에 그려지는 데이터의 개수 
let tick = 0; // 도착한 데이터의 개수임, tick의 범위는 0에서 99까지만 

function drawChart() {
	ctx = document.getElementById('canvas').getContext('2d');
	chart = new Chart(ctx, config);
	init();
} 

function init() { // chart.data.labels의 크기를 LABEL_SIZE로 만들고 0~19까지 레이블 붙이기
	for(let i=0; i<LABEL_SIZE; i++) {
		chart.data.labels[i] = i;
	}
	chart.update();
}

function addChartData(value, index) {
	tick++; // 도착한 데이터의 개수 증가
	tick %= 100; // tick의 범위는 0에서 99까지만. 100보다 크면 다시 0부터 시작
	let n = chart.data.datasets[index].data.length; // 현재 데이터의 개수 
	if(n < LABEL_SIZE) // 현재 데이터 개수가 LABEL_SIZE보다 작은 경우
		chart.data.datasets[index].data.push(value);
	else { // 현재 데이터 개수가 LABEL_SIZE를 넘어서는 경우
		// 새 데이터 value 삽입
		chart.data.datasets[index].data.push(value); // value를 data[]의 맨 끝에 추가
		chart.data.datasets[index].data.shift(); // data[]의 맨 앞에 있는 데이터 제거

		// 레이블 삽입
		chart.data.labels.push(tick); // tick 값을 labels[]의 맨 끝에 추가
		chart.data.labels.shift(); // labels[]의 맨 앞에 있는 값 제거
	}
	chart.update();
}
function hideshow() {
    try {
        let canvas = document.getElementById('canvas');

        if (!canvas) {
            console.error('Canvas element not found');
            return;
        }

        // 현재 display 속성이 "none"이거나 빈 문자열이면
        if (canvas.style.display === "none" || canvas.style.display === "") {
            canvas.style.display = "inline-block";
        } else {
            canvas.style.display = "none";
        }
    } catch (error) {
        console.error('An error occurred in hideshow:', error);
    }
}
window.addEventListener("load", drawChart); // load 이벤트가 발생하면 drawChart() 호출하도록 등록
