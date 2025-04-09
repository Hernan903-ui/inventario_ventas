class App {
    constructor() {
        this.initRouter();
        this.loadInitialView();
    }

    initRouter() {
        window.addEventListener("hashchange", () => this.loadView());
    }

    loadInitialView() {
        const defaultView = window.location.hash.substring(1) || "products";
        this.loadView(defaultView);
    }

    async loadView() {
        const viewName = window.location.hash.substring(1) || "products";
        const viewPath = `/views/${viewName}.html`;

        try {
            const response = await fetch(viewPath);
            if (!response.ok) throw new Error("Vista no encontrada");
            
            const html = await response.text();
            document.getElementById("mainContent").innerHTML = html;

            this.initViewModule(viewName);
        } catch (error) {
            console.error("Error cargando vista:", error);
            document.getElementById("mainContent").innerHTML = "<h2>Error cargando la vista</h2>";
        }
    }

    initViewModule(viewName) {
        switch(viewName) {
            case "products":
                new Products();
                break;
            case "analytics":
                new Analytics();
                break;
            default:
                console.warn("Módulo no implementado para:", viewName);
        }
    }
}

// Iniciar aplicación
new App();