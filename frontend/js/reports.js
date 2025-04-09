// Función para inicializar gráficos
function initializeCharts() {
    const ctx = document.getElementById('monthlySalesChart').getContext('2d');
    const monthlySalesChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio'],
            datasets: [{
                label: 'Ventas Mensuales ($)',
                data: [1200, 1500, 1800, 1600, 2000, 2200],
                backgroundColor: '#4CAF50',
                borderColor: '#4CAF50',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Función para exportar el reporte a PDF (usando jsPDF)
function exportToPDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Agregar contenido al PDF
    doc.text('Reporte de Ventas', 10, 10);
    doc.text('-----------------', 10, 20);
    doc.text('Mes   | Ventas', 10, 30);
    doc.text('Enero | $1200', 10, 40);
    doc.text('Febrero | $1500', 10, 50);
    doc.text('Marzo | $1800', 10, 60);

    // Guardar el PDF
    doc.save('reporte_ventas.pdf');
}

// Asociar el botón de exportar con la función
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    const exportButton = document.querySelector('.btn-export');
    if (exportButton) {
        exportButton.addEventListener('click', exportToPDF);
    }
});