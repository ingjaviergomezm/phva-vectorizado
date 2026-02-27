import json
import os
from collections import Counter

LEARNING_LOG_FILE = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm\reportes_agente\router_learning.json"
PHVA_FILE = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm\ROUTER_PHVA.md"

def analyze_learning():
    if not os.path.exists(LEARNING_LOG_FILE):
        print("ℹ️ No hay datos de aprendizaje aún. El router sigue en su fase base.")
        return

    with open(LEARNING_LOG_FILE, "r") as f:
        logs = json.load(f)

    print(f"📊 Analizando {len(logs)} fallos T1 registrados...")
    
    # Contar fallos por modelo
    model_fails = Counter([l['model'] for l in logs])
    print("\n❌ Fallos por Modelo:")
    for model, count in model_fails.items():
        print(f" - {model}: {count}")

    # Identificar keywords comunes en fallos
    all_text = " ".join([l['prompt_hint'] for l in logs]).lower()
    common_words = Counter(all_text.split()).most_common(10)
    
    print("\n🔍 Palabras clave en prompts fallidos:")
    for word, count in common_words:
        if len(word) > 3:
            print(f" - '{word}': {count} veces")

    print("\n💡 Recomendación PHVA:")
    if model_fails.get('gpt-4o-mini', 0) > 5:
        print(" -> ALERTA: gpt-4o-mini está fallando bajo carga. Revisar límites de tokens en ROUTER_PHVA.md")
    
    print("-" * 40)

if __name__ == "__main__":
    analyze_learning()
