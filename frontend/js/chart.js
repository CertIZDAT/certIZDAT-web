const data_array = data.split(", ").map(Number)
const dates_array = dates.split(", ").map(String)

const ctx = document.getElementById('statistic-chart');
new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates_array,
        datasets: [{
            label: 'CA Amount',
            data: data_array,
            borderWidth: 1,
            borderColor: 'rgb(255, 0, 0)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                min: 1,
                max: 31,
                ticks: {
                    maxRotation: 75,
                    minRotation: 75
                }
            },
            y: {
                beginAtZero: true,
                min: 0,
                max: 1500,
                ticks: {
                    autoSkip: false,
                    maxRotation: 90,
                    minRotation: 90
                }
            }
        }
    }
});
