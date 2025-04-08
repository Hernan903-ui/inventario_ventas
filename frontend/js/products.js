class Products {
    constructor() {
        this.tableBody = document.getElementById('productsTableBody');
        this.productForm = document.getElementById('productForm');
        this.scanButton = document.getElementById('scanBarcode');
        this.init();
    }

    async init() {
        await this.loadProducts();
        this.setupEventListeners();
        this.checkLowStock();
    }

    async loadProducts() {
        try {
            const response = await fetch('/api/products', {
                headers: this.getAuthHeaders()
            });
            
            const products = await response.json();
            this.renderProducts(products);
        } catch (error) {
            console.error('Error loading products:', error);
        }
    }

    renderProducts(products) {
        this.tableBody.innerHTML = products.map(product => `
            <tr>
                <td>${product.barcode}</td>
                <td>${product.name}</td>
                <td>${product.stock}</td>
                <td>${product.sale_price}</td>
                <td>
                    <button data-edit="${product.id}">Editar</button>
                    <button data-stock="${product.id}">Actualizar Stock</button>
                </td>
            </tr>
        `).join('');
    }

    setupEventListeners() {
        // Formulario de producto
        this.productForm?.addEventListener('submit', e => this.handleProductSubmit(e));
        
        // Botón de escanear
        this.scanButton?.addEventListener('click', () => this.initBarcodeScanner());
        
        // Eventos delegados para botones
        document.addEventListener('click', async e => {
            if (e.target.matches('[data-edit]')) {
                this.handleEditProduct(e.target.dataset.edit);
            }
            if (e.target.matches('[data-stock]')) {
                this.handleUpdateStock(e.target.dataset.stock);
            }
        });
    }

    async handleProductSubmit(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch('/api/products', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    ...this.getAuthHeaders()
                },
                body: JSON.stringify({
                    name: formData.get('name'),
                    barcode: formData.get('barcode'),
                    cost_price: parseFloat(formData.get('cost_price')),
                    sale_price: parseFloat(formData.get('sale_price')),
                    stock: parseInt(formData.get('stock')),
                    supplier_id: parseInt(formData.get('supplier_id'))
                })
            });
            
            if (response.ok) {
                this.loadProducts();
                e.target.reset();
            }
        } catch (error) {
            console.error('Error saving product:', error);
        }
    }

    initBarcodeScanner() {
        Quagga.init({
            inputStream: {
                name: "Live",
                type: "LiveStream",
                target: document.querySelector('#scannerContainer')
            },
            decoder: {
                readers: ['ean_reader']
            }
        }, err => {
            if (err) return console.error('Error iniciando escáner:', err);
            
            Quagga.start();
            Quagga.onDetected(data => {
                document.getElementById('barcode').value = data.codeResult.code;
                Quagga.stop();
            });
        });
    }

    getAuthHeaders() {
        return {
            'Authorization': localStorage.getItem('token')
        };
    }

    async checkLowStock() {
        try {
            const response = await fetch('/api/products/low-stock', {
                headers: this.getAuthHeaders()
            });
            
            const lowStockProducts = await response.json();
            if (lowStockProducts.length > 0) {
                this.showStockAlert(lowStockProducts);
            }
        } catch (error) {
            console.error('Error checking stock:', error);
        }
    }

    showStockAlert(products) {
        const alertHtml = `
            <div class="stock-alert">
                <h3>Stock Bajo!</h3>
                <ul>
                    ${products.map(p => `<li>${p.name} - ${p.stock} unidades</li>`).join('')}
                </ul>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', alertHtml);
    }
}