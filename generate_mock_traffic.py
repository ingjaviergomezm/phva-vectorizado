import json
import os
import random
from datetime import datetime, timedelta

# Configuración de rutas
LOG_DIR = os.path.join(os.getcwd(), "reportes_agente")
os.makedirs(LOG_DIR, exist_ok=True)
HISTORY_FILE = os.path.join(LOG_DIR, "history_metrics.json")
LIVE_FILE = os.path.join(LOG_DIR, "live_dashboard_data.json")

MODELS = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gemini/gemini-flash-latest": {"input": 0.075, "output": 0.30},
    "perplexity/sonar-pro": {"input": 5.0, "output": 15.0},
    "ollama/llama3.1:8b": {"input": 0.0, "output": 0.0}
}
PRO_PRICING = {"input": 5.0, "output": 15.0}

def generate_mock_data(count=50):
    data = []
    base_time = datetime.now() - timedelta(days=2) # Empezar hace 2 días
    
    for i in range(count):
        # Avanzar el tiempo aleatoriamente entre 10 min y 2 horas
        base_time += timedelta(minutes=random.randint(10, 120))
        if base_time > datetime.now(): break
        
        model_name = random.choice(list(MODELS.keys()))
        pricing = MODELS[model_name]
        
        # Tokens aleatorios
        in_t = random.randint(500, 5000)
        out_t = random.randint(200, 2000)
        
        real_cost = ((in_t / 1_000_000) * pricing["input"]) + ((out_t / 1_000_000) * pricing["output"])
        pro_cost = ((in_t / 1_000_000) * PRO_PRICING["input"]) + ((out_t / 1_000_000) * PRO_PRICING["output"])
        
        status = "SUCCESS"
        if random.random() < 0.1: status = "FAILURE"
        elif random.random() < 0.15: status = "RECOVERED"
        
        entry = {
            "timestamp": base_time.isoformat(),
            "type": "REQUEST" if status != "RECOVERED" else "FALLBACK",
            "model": model_name,
            "status": status,
            "message": "Simulated traffic event" if status == "SUCCESS" else "Error simulation",
            "cost": round(real_cost, 6),
            "pro_cost": round(pro_cost, 6),
            "latency": round(random.uniform(0.5, 5.0), 2)
        }
        data.append(entry)
    
    # Guardar en histórico
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Guardar últimos 50 en live
    with open(LIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data[-50:], f, indent=2, ensure_ascii=False)

    print(f"✅ Generados {len(data)} eventos de prueba en {HISTORY_FILE}")

if __name__ == "__main__":
    generate_mock_data(100)
