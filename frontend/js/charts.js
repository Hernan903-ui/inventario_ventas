class ChartUtils {
    static initCharts() {
        Chart.defaults.global.responsive = true;
        Chart.defaults.global.maintainAspectRatio = false;
    }

    static createBarChart(ctx, labels, data, label) {
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    static createPieChart(ctx, labels, data) {
        return new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#ff6384',
                        '#36a2eb',
                        '#cc65fe',
                        '#ffce56'
                    ]
                }]
            }
        });
    }
}

ChartUtils.initCharts();