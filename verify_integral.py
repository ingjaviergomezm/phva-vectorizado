import json
import os
import random
from datetime import datetime, timedelta
from telemetry import update_json_dashboard, COST_TABLE

def run_simulation(events_count=100):
    print(f"🚀 Iniciando simulación de {events_count} eventos integrales...")
    
    # Limpiar archivos previos para empezar de cero en esta verificación
    LOG_DIR = os.path.join(os.getcwd(), "reportes_agente")
    for f in ["live_dashboard_data.json", "history_metrics.json", "daily_stats.json"]:
        path = os.path.join(LOG_DIR, f)
        if os.path.exists(path): os.remove(path)

    models = ["gpt-4o-mini", "gemini/gemini-flash-latest", "perplexity/sonar-pro", "ollama/llama3.1:8b"]
    
    # Generar datos de los últimos 5 días
    start_time = datetime.now() - timedelta(days=5)
    
    for i in range(events_count):
        # Avanzar el tiempo aleatoriamente
        current_time = start_time + timedelta(minutes=random.randint(10, 180))
        start_time = current_time
        if current_time > datetime.now(): break
        
        model = random.choice(models)
        pricing = COST_TABLE.get(model, {"input": 10.0, "output": 30.0})
        
        in_t = random.randint(100, 5000)
        out_t = random.randint(50, 2000)
        
        real_cost = ((in_t / 1_000_000) * pricing["input"]) + ((out_t / 1_000_000) * pricing["output"])
        pro_cost = ((in_t / 1_000_000) * 5.0) + ((out_t / 1_000_000) * 15.0)
        
        status = "SUCCESS"
        event_type = "REQUEST"
        if random.random() < 0.1: # 10% fallos
            status = "FAILURE"
        elif random.random() < 0.2: # 20% fallbacks
            status = "RECOVERED"
            event_type = "FALLBACK"
            real_cost = 0.0 # Asumimos recuperación local barata
            pro_cost = pro_cost # Pero el Pro seguiría costando lo mismo

        # Mock de update_json_dashboard para poder inyectar timestamps pasados
        # (Modificamos temporalmente el sistema para la simulación)
        inject_event(current_time, event_type, model, status, "Evento simulado integral", real_cost, pro_cost, random.uniform(0.5, 4.0))

    print("✅ Simulación integral completada.")

def inject_event(ts, event_type, model, status, message, cost, pro_cost, latency):
    LOG_DIR = os.path.join(os.getcwd(), "reportes_agente")
    JSON_EVENTS_FILE = os.path.join(LOG_DIR, "live_dashboard_data.json")
    HISTORY_FILE = os.path.join(LOG_DIR, "history_metrics.json")
    DAILY_STATS_FILE = os.path.join(LOG_DIR, "daily_stats.json")

    new_event = {
        "timestamp": ts.isoformat(),
        "type": event_type,
        "model": model,
        "status": status,
        "message": message,
        "cost": round(cost, 6),
        "pro_cost": round(pro_cost, 6),
        "latency": round(latency, 2)
    }

    # Live & History
    for f_path in [JSON_EVENTS_FILE, HISTORY_FILE]:
        data = []
        if os.path.exists(f_path):
            with open(f_path, "r") as f: data = json.load(f)
        data.append(new_event)
        with open(f_path, "w") as f: json.dump(data, f, indent=2)

    # Daily Stats Aggregator
    today_key = ts.strftime('%Y-%m-%d')
    stats = {}
    if os.path.exists(DAILY_STATS_FILE):
        with open(DAILY_STATS_FILE, "r") as f: stats = json.load(f)
    if today_key not in stats:
        stats[today_key] = {"total_cost":0.0, "total_pro_cost":0.0, "requests":0, "successes":0, "fallbacks":0, "avg_latency":0.0}
    
    s = stats[today_key]
    n = s["requests"]
    s["total_cost"] += cost
    s["total_pro_cost"] += pro_cost
    s["avg_latency"] = (s["avg_latency"] * n + latency) / (n + 1)
    s["requests"] += 1
    if status == "SUCCESS": s["successes"] += 1
    if event_type == "FALLBACK": s["fallbacks"] += 1
    with open(DAILY_STATS_FILE, "w") as f: json.dump(stats, f, indent=2)

if __name__ == "__main__":
    run_simulation(80)
