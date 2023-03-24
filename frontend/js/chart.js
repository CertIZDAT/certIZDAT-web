console.log(data);

const ctx = document.getElementById('statistic-chart');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['2023-03-20', '21', '22', '23', '24', '25', '26', '27', '28', '29'],
        datasets: [{
            label: 'CA Amount',
            data: [12, 19, 3, 5, 2, 3],
            borderWidth: 1,
            borderColor: 'rgb(255, 0, 0)',
            tension: 0.5
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        onClick: (e) => {
            const canvasPosition = Chart.helpers.getRelativePosition(e, chart);
            const dataX = chart.scales.x.getValueForPixel(canvasPosition.x);
            const dataY = chart.scales.y.getValueForPixel(canvasPosition.y);
        }
    }
});
