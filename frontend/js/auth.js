class Auth {
    constructor() {
        this.loginForm = document.getElementById('loginForm');
        this.registerForm = document.getElementById('registerForm');
        this.initEventListeners();
    }

    initEventListeners() {
        if (this.loginForm) {
            this.loginForm.addEventListener('submit', e => this.handleLogin(e));
        }
        
        if (this.registerForm) {
            this.registerForm.addEventListener('submit', e => this.handleRegister(e));
        }
    }

    async handleLogin(e) {
        e.preventDefault();
        const email = e.target.email.value.trim();
        const password = e.target.password.value;
    
        // Validaciones
        if (!email || !password) {
            return alert('Todos los campos son requeridos');
        }
        if (!/\S+@\S+\.\S+/.test(email)) {
            return alert('Email inválido');
        }
    
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            
            if (!response.ok) throw new Error('Error en credenciales');
            
            const data = await response.json();
            localStorage.setItem('token', data.token);
            window.location.href = '/#products';
            
        } catch (error) {
            alert(error.message);
        }
    }

    async handleRegister(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    business_name: formData.get('business_name'),
                    first_name: formData.get('first_name'),
                    last_name: formData.get('last_name'),
                    email: formData.get('email'),
                    password: formData.get('password')
                })
            });
            
            if (response.ok) {
                alert('Registro exitoso! Por favor inicie sesión');
                window.location.hash = 'login';
            } else {
                const error = await response.json();
                alert(error.error);
            }
        } catch (error) {
            console.error('Register error:', error);
        }
    }
}