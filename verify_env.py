import sys
import platform
import urllib.request
import urllib.error

def print_status(component, status, details=""):
    color = "\033[92m" if status else "\033[91m"
    reset = "\033[0m"
    icon = "[OK]" if status else "[FAIL]"
    print(f"{color}{icon} {component}{reset} {details}")

def verify_environment():
    print("=== Iniciando Validación de QA: Entorno Local ===\n")

    # 1. Verificar versión de Python
    py_version = sys.version_info
    py_ok = py_version.major == 3 and py_version.minor >= 10
    print_status("Python Version", py_ok, f"({platform.python_version()}) Se requiere >= 3.10")

    # 2. Verificar dependencias Core
    deps = ["praisonai", "praisonaiagents", "litellm", "mcp"]
    for dep in deps:
        try:
            __import__(dep.replace("-", "_"))
            print_status(f"Librería: {dep}", True)
        except ImportError:
            print_status(f"Librería: {dep}", False, "Falta instalar")

    # 3. Verificar conexión con Ollama Local
    ollama_url = "http://localhost:11434"
    try:
        req = urllib.request.Request(ollama_url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                print_status("Ollama Local", True, f"Respondiendo en {ollama_url}")
            else:
                print_status("Ollama Local", False, f"Respuesta inesperada: HTTP {response.status}")
    except urllib.error.URLError as e:
        print_status("Ollama Local", False, f"No se pudo conectar: {e.reason}")
    except Exception as e:
        print_status("Ollama Local", False, f"Error desconocido: {e}")

if __name__ == "__main__":
    verify_environment()
