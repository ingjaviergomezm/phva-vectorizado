import http.server
import socketserver
import webbrowser
import os
import sys

# Rutas estándar de Antigravity
BASE_DIR = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm"
PORT = 8000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

def start_dashboard():
    os.chdir(BASE_DIR)
    
    # Verificar existencia del dashboard
    if not os.path.exists("dashboard_agente.html"):
        print(f"Error: No se encuentra dashboard_agente.html en {BASE_DIR}")
        return

    try:
        with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
            url = f"http://localhost:{PORT}/dashboard_agente.html"
            print(f"🚀 Dashboard de Antigravity activo en: {url}")
            print("Presiona Ctrl+C para detener el servidor.")
            
            # Abrir navegador automáticamente
            webbrowser.open(url)
            
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:
            print(f"El puerto {PORT} ya está en uso. Intenta cerrar otras instancias.")
        else:
            print(f"Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR, exist_ok=True)
    start_dashboard()
