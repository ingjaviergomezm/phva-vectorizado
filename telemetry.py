import os
import logging
import json
from datetime import datetime, timedelta
import litellm

# ==============================================================================
# 1. CONFIGURACIÓN DEL LOGGING CENTRALIZADO
# ==============================================================================
# Uso de ruta absoluta para asegurar persistencia integral
BASE_PROJECT_DIR = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm"
LOG_DIR = os.path.join(BASE_PROJECT_DIR, "reportes_agente")
os.makedirs(LOG_DIR, exist_ok=True)

# Archivos de Datos
JSON_EVENTS_FILE = os.path.join(LOG_DIR, "live_dashboard_data.json")
HISTORY_FILE = os.path.join(LOG_DIR, "history_metrics.json")
DAILY_STATS_FILE = os.path.join(LOG_DIR, "daily_stats.json")
LEARNING_LOG_FILE = os.path.join(LOG_DIR, "router_learning.json") # Memoria para PHVA de Puntería

# Configuración Logging Estándar
LOG_FILE = os.path.join(LOG_DIR, f"telemetria_{datetime.now().strftime('%Y%m%d')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True
)
logger = logging.getLogger("AntigravityTelemetry")

# ==============================================================================
# 2. TABLA DE COSTOS INTEGRAL (USD por 1M tokens) - Mapeo .env
# ==============================================================================
COST_TABLE = {
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gemini/gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini/gemini-flash-latest": {"input": 0.075, "output": 0.30},
    "gemini/gemini-1.5-pro": {"input": 1.25, "output": 3.75},
    "perplexity/sonar-pro": {"input": 5.0, "output": 15.0},
    "ollama/llama3.1:8b": {"input": 0.0, "output": 0.0},
    "ollama/qwen2.5": {"input": 0.0, "output": 0.0},
    "ollama/deepseek-r1:14b": {"input": 0.0, "output": 0.0}
}

# BENCHMARK PRO (Whitepaper: $5/$15)
PRO_MODEL_PRICING = {"input": 5.0, "output": 15.0}

# SEGURIDAD (Item 7): Límites de Presupuesto
DAILY_BUDGET_LIMIT = 2.00  # Máximo de $2 USD por día

def calculate_costs(model, input_tokens, output_tokens):
    """Calcula el costo real y el proyectado (Pro) integralmente."""
    pricing = COST_TABLE.get(model, {"input": 10.0, "output": 30.0}) # Default caro si no existe
    real_cost = ((input_tokens / 1_000_000) * pricing["input"]) + ((output_tokens / 1_000_000) * pricing["output"])
    pro_cost = ((input_tokens / 1_000_000) * PRO_MODEL_PRICING["input"]) + ((output_tokens / 1_000_000) * PRO_MODEL_PRICING["output"])
    return real_cost, pro_cost

def check_budget():
    """Item 7: Verifica si el costo acumulado hoy ha superado el límite de seguridad."""
    try:
        if not os.path.exists(DAILY_STATS_FILE): return True
        with open(DAILY_STATS_FILE, "r") as f:
            stats = json.load(f)
        today_key = datetime.now().strftime('%Y-%m-%d')
        if today_key in stats:
            current_cost = stats[today_key].get("total_cost", 0.0)
            if current_cost >= DAILY_BUDGET_LIMIT:
                logger.warning(f"🚨 CIRCUIT BREAKER: Presupuesto diario excedido (${current_cost:.2f} >= ${DAILY_BUDGET_LIMIT:.2f})")
                return False
        return True
    except Exception as e:
        logger.error(f"Error checking budget: {e}")
        return True # Por seguridad, permitimos si el tracker falla

# ==============================================================================
# 3. MOTOR DE AGREGACIÓN (Daily/Monthly Stats)
# ==============================================================================
def aggregate_stats(new_event):
    """Agrega estadísticas diarias para análisis a largo plazo."""
    try:
        today_key = datetime.now().strftime('%Y-%m-%d')
        stats = {}
        if os.path.exists(DAILY_STATS_FILE):
            with open(DAILY_STATS_FILE, "r") as f:
                stats = json.load(f)
        
        if today_key not in stats:
            stats[today_key] = {
                "total_cost": 0.0,
                "total_pro_cost": 0.0,
                "requests": 0,
                "successes": 0,
                "fallbacks": 0,
                "avg_latency": 0.0
            }
        
        s = stats[today_key]
        n = s["requests"]
        s["total_cost"] += new_event["cost"]
        s["total_pro_cost"] += new_event["pro_cost"]
        s["avg_latency"] = (s["avg_latency"] * n + new_event["latency"]) / (n + 1)
        s["requests"] += 1
        if new_event["status"] == "SUCCESS": s["successes"] += 1
        if new_event["type"] == "FALLBACK": s["fallbacks"] += 1
        
        with open(DAILY_STATS_FILE, "w") as f:
            json.dump(stats, f, indent=2)
    except Exception as e:
        logger.error(f"Error en agregación diaria: {e}")

def update_json_dashboard(event_type, model, status, message, cost=0.0, pro_cost=0.0, latency=0.0):
    """Persistencia de eventos en tres niveles."""
    try:
        new_event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "model": model,
            "status": status,
            "message": message,
            "cost": round(cost, 6),
            "pro_cost": round(pro_cost, 6),
            "latency": round(latency, 2)
        }
        
        # 1. Live Events (Últimos 100)
        events = []
        if os.path.exists(JSON_EVENTS_FILE):
            with open(JSON_EVENTS_FILE, "r") as f: events = json.load(f)
        events = (events + [new_event])[-100:]
        with open(JSON_EVENTS_FILE, "w") as f: json.dump(events, f, indent=2)
        
        # 2. History (Últimos 1000 para Charts detallados)
        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f: history = json.load(f)
        history = (history + [new_event])[-1000:]
        with open(HISTORY_FILE, "w") as f: json.dump(history, f, indent=2)
        
        # 3. Daily Stats (Para vista de meses/años)
        aggregate_stats(new_event)

    except Exception as e:
        logger.error(f"Error actualizando persistencia integral: {e}")

def log_router_failure(model, task_type, error_msg, prompt_hint):
    """Item 8: Captura el error para que el router aprenda (Ciclo PHVA)."""
    try:
        learning_data = []
        if os.path.exists(LEARNING_LOG_FILE):
            with open(LEARNING_LOG_FILE, "r") as f:
                learning_data = json.load(f)
        
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "task_type": task_type,
            "error": error_msg,
            "prompt_hint": prompt_hint[:100] + "..." # Solo un hint por privacidad/tokens
        }
        
        learning_data = (learning_data + [new_entry])[-500:] # Mantener últimos 500 fallos
        with open(LEARNING_LOG_FILE, "w") as f:
            json.dump(learning_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error en log_router_failure: {e}")

# ==============================================================================
# 4. CALLBACKS DE LITELLM
# ==============================================================================
def success_callback(kwargs, completion_response, start_time, end_time):
    try:
        model = kwargs.get("model", "unknown")
        usage = getattr(completion_response, "usage", {})
        prompt_tokens = getattr(usage, "prompt_tokens", 0)
        completion_tokens = getattr(usage, "completion_tokens", 0)
        latency = (end_time - start_time).total_seconds()
        real_cost, pro_cost = calculate_costs(model, prompt_tokens, completion_tokens)
        
        update_json_dashboard("REQUEST", model, "SUCCESS", "Petición procesada", real_cost, pro_cost, latency)
        logger.info(f"Metrica: Model={model} | Real=${real_cost:.6f} | Pro=${pro_cost:.6f}")
    except Exception as e:
        logger.error(f"Error success_callback: {e}")

def failure_callback(kwargs, exception, start_time, end_time):
    try:
        model = kwargs.get("model", "unknown")
        latency = (end_time - start_time).total_seconds()
        err_msg = str(exception)
        update_json_dashboard("REQUEST", model, "FAILURE", err_msg, 0.0, 0.0, latency)
        
        # PHVA Learning (Solo si es T1, detectado por la falta de 'fallback' en kwargs)
        prompt = kwargs.get("messages", [{}])[0].get("content", "")
        log_router_failure(model, "unknown", err_msg, prompt)
        
        logger.error(f"Fallo Metrica: {model} | {err_msg}")
    except Exception as e:
        logger.error(f"Error failure_callback: {e}")

def init_telemetry():
    litellm.success_callback = [success_callback]
    litellm.failure_callback = [failure_callback]
    logger.info("### Antigravity Telemetry v4.0 (Integral & Analytics) Activa ###")

if __name__ == "__main__":
    init_telemetry()
    # Simulación de prueba integral
    update_json_dashboard("REQUEST", "gpt-4o", "SUCCESS", "Prueba integral", 0.002, 0.015, 1.5)
    print("Telemetría configurada.")
