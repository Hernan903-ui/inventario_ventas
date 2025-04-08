const CACHE_NAME = 'inventory-v2';
const OFFLINE_PAGE = '/index.html';
const ASSETS = [
  '/',
  '/index.html',
  '/css/styles.css',
  '/js/app.js',
  '/js/auth.js',
  '/js/products.js',
  '/js/analytics.js',
  '/js/charts.js',
  '/libs/chart.min.js',
  '/libs/quagga.min.js',
  '/libs/FileSaver.min.js',
  '/images/logo.png',
  '/images/offline.png'
];

// Instalación del Service Worker y caché inicial
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Almacenando en caché recursos críticos');
        return cache.addAll(ASSETS);
      })
      .then(() => self.skipWaiting())
  );
});

// Activación y limpieza de cachés antiguos
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] Eliminando caché antigua:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Estrategia de caché: Cache First with Network Fallback
self.addEventListener('fetch', (event) => {
  // Ignorar solicitudes de chrome-extension y solicitudes POST
  if (event.request.url.includes('chrome-extension') || event.request.method === 'POST') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(cachedResponse => {
        // Devuelve respuesta en caché si existe
        if (cachedResponse) {
          console.log(`[Service Worker] Recuperando de caché: ${event.request.url}`);
          return cachedResponse;
        }

        // Clona la solicitud para hacer fetch
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest)
          .then(response => {
            // Verifica respuesta válida
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clona la respuesta para almacenar en caché
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                console.log(`[Service Worker] Almacenando en caché: ${event.request.url}`);
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch(() => {
            // Manejo especial para navegación offline
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_PAGE);
            }
            return new Response('Offline', {
              status: 503,
              statusText: 'Service Unavailable',
              headers: new Headers({ 'Content-Type': 'text/plain' })
            });
          });
      })
  );
});

// Manejo de sincronización en segundo plano
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-data') {
    console.log('[Service Worker] Sincronizando datos en segundo plano');
    // Aquí iría la lógica de sincronización
  }
});

// Manejo de notificaciones push
self.addEventListener('push', (event) => {
  const data = event.data.json();
  const title = data.title || 'Notificación del Sistema';
  const options = {
    body: data.body || 'Nueva actualización disponible',
    icon: '/images/logo.png',
    badge: '/images/badge.png'
  };

  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});