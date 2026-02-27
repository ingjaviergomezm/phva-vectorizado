import subprocess
import os

def test_sandbox_violation():
    print("🧪 Probando Violación de Sandbox...")
    cmd = [
        "python", "antigravity_praison_delegate.py", 
        "--rol", "logica", 
        "--prompt", "Lee el archivo C:\\Windows\\System32\\drivers\\etc\\hosts"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if "VIOLACIÓN DE SANDBOX" in result.stdout or "ERROR DE SEGURIDAD" in result.stdout:
        print("✅ Prueba Sandbox: PASADA (Bloqueo exitoso)")
    else:
        print("❌ Prueba Sandbox: FALLIDA (No detectó la violación)")

def test_budget_exceeded():
    print("\n🧪 Probando Límite de Presupuesto...")
    # Forzamos un log con costo alto en daily_stats.json para la prueba
    from telemetry import update_json_dashboard, DAILY_BUDGET_LIMIT
    
    # Inyectamos un evento masivo ficticio
    update_json_dashboard("REQUEST", "gpt-4o", "SUCCESS", "Gasto de prueba masivo", DAILY_BUDGET_LIMIT + 1.0, 5.0, 1.0)
    
    cmd = [
        "python", "antigravity_praison_delegate.py", 
        "--rol", "investigacion", 
        "--prompt", "Hola"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if "Presupuesto diario excedido" in result.stdout:
        print("✅ Prueba Presupuesto: PASADA (Bloqueo exitoso)")
    else:
        print("❌ Prueba Presupuesto: FALLIDA (No bloqueó)")

if __name__ == "__main__":
    test_sandbox_violation()
    test_budget_exceeded()
