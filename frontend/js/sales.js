class SalesManager {
    constructor() {
        this.cart = [];
        this.products = [];
        this.init();
    }

    async init() {
        await this.loadProducts();
        this.setupEventListeners();
    }

    async loadProducts() {
        try {
            const response = await fetch('/api/products', {
                headers: {
                    'Authorization': localStorage.getItem('token')
                }
            });
            this.products = await response.json();
            this.renderProducts();
        } catch (error) {
            console.error('Error loading products:', error);
        }
    }

    renderProducts() {
        const container = document.querySelector('.products-grid');
        container.innerHTML = this.products.map(product => `
            <div class="product-card">
                <h3>${product.name}</h3>
                <p>Stock: ${product.stock}</p>
                <p>$${product.price}</p>
            </div>
        `).join('');
    }
}