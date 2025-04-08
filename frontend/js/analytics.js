class Analytics {
    constructor() {
        this.salesChart = null;
        this.stockChart = null;
        this.init();
    }

    async init() {
        await this.loadSalesData();
        await this.loadStockAnalysis();
        await this.loadDemandAnalysis();
    }

    async loadSalesData() {
        try {
            const response = await fetch('/api/analytics/sales-data', {
                headers: { 'Authorization': localStorage.getItem('token') }
            });
            
            const data = await response.json();
            this.renderSalesChart(data);
        } catch (error) {
            console.error('Error loading sales data:', error);
        }
    }

    renderSalesChart(data) {
        const ctx = document.getElementById('salesChart').getContext('2d');
        
        if (this.salesChart) this.salesChart.destroy();
        
        this.salesChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.product),
                datasets: [{
                    label: 'Ventas últimos 30 días',
                    data: data.map(item => item.sales),
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    async loadStockAnalysis() {
        try {
            const response = await fetch('/api/analytics/stock-analysis', {
                headers: { 'Authorization': localStorage.getItem('token') }
            });
            
            const data = await response.json();
            this.renderStockChart(data);
        } catch (error) {
            console.error('Error loading stock analysis:', error);
        }
    }

    renderStockChart(data) {
        const ctx = document.getElementById('stockChart').getContext('2d');
        
        if (this.stockChart) this.stockChart.destroy();
        
        this.stockChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Stock Bajo', 'Stock Suficiente'],
                datasets: [{
                    data: [data.low_stock, data.total_products - data.low_stock],
                    backgroundColor: ['#ff6384', '#36a2eb']
                }]
            }
        });
    }

    async loadDemandAnalysis() {
        try {
            const response = await fetch('/api/analytics/demand-analysis', {
                headers: { 'Authorization': localStorage.getItem('token') }
            });
            
            const data = await response.json();
            this.renderDemandLists(data);
        } catch (error) {
            console.error('Error loading demand analysis:', error);
        }
    }

    renderDemandLists(data) {
        const topList = document.getElementById('topProductsList');
        const lowList = document.getElementById('lowProductsList');
        
        topList.innerHTML = data.top_products.map(p => `
            <li>${p.name} - ${p.sales} ventas</li>
        `).join('');
        
        lowList.innerHTML = data.low_products.map(p => `
            <li>${p.name} - ${p.sales} ventas</li>
        `).join('');
    }
}