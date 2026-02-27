import os
from praisonaiagents import Agent

# Explicación:
# PraisonAI usa LiteLLM debajo del capó para las llamadas a los modelos.
# LiteLLM soporta 'Fallbacks' (Modelos de Respaldo) enviando una lista de strings
# como nombre de modelo. Si el principal falla, intenta el siguiente automáticamente.

# Configuración del Enrutador (Router) Cloud-First, Local-Backup
MODELO_RAZONAMIENTO_COMPLEJO = ["gpt-4o-mini", "ollama/deepseek-r1:14b"]  
MODELO_TAREAS_VOLUMEN = ["gemini/gemini-flash-latest", "ollama/llama3.1:8b"]
MODELO_INVESTIGACION = ["perplexity/sonar-pro"]

def generar_agente_router(tipo_tarea: str) -> Agent:
    """
    Asigna dinámicamente el stack de modelos según la clasificación de la tarea.
    Implementamos el Vacío 1 (Estrategia de Fallback) del QA.
    """
    if tipo_tarea == "compleja":
        modelo_list = MODELO_RAZONAMIENTO_COMPLEJO
        instrucciones = "Eres un razonador lógico de backend. Piensa paso a paso."
        nombre = "Senior Backend"
    elif tipo_tarea == "investigacion":
        modelo_list = MODELO_INVESTIGACION
        instrucciones = "Usa internet para dar información veraz y actual con enlaces."
        nombre = "Buscador Online"
    else:
        # Default de alto volumen (tareas largas, formateo JSON, corrección textos)
        modelo_list = MODELO_TAREAS_VOLUMEN
        instrucciones = "Procesa los datos rápidamente sin agregar reflexiones inútiles."
        nombre = "Procesador de Datos"
        
    agente = Agent(
        name=nombre,
        role="Asistente de Enrutamiento Dinámico",
        goal="Ejecutar la tarea con máxima eficiencia de costos y velocidad.",
        backstory="Eres parte de un sistema multi-agente tolerante a fallos.",
        instructions=instrucciones,
        llm=modelo_list # PraisonAI 1.5.15 y superiores soportan List[str] para fallback
    )
    return agente

def main():
    print("=== Iniciando Router Agent (Cloud First -> Local Backup) ===\n")
    
    # 1. Prueba de Alta Velocidad (Gemini -> Llama3)
    agente_volumen = generar_agente_router("volumen")
    print(f"Lanzando Obrero de Datos (Modelos: {MODELO_TAREAS_VOLUMEN})")
    
    try:
        resultado = agente_volumen.start("Saca el promedio de 1+4+10.")
        print(f"\nRespuesta del Obrero:\n{resultado}\n")
    except Exception as e:
        print(f"\nFallback falló en el Obrero de Datos: {str(e)}\n")

    print("-" * 50)
    
    # 2. Prueba de Razonamiento (OpenAI -> DeepSeek)
    agente_backend = generar_agente_router("compleja")
    print(f"Lanzando Lógico Avanzado (Modelos: {MODELO_RAZONAMIENTO_COMPLEJO})")
    
    try:
        resultado_logico = agente_backend.start("Si Juan es más alto que Pedro, y Pedro es igual a Luis. ¿Quién es el más bajo?")
        print(f"\nRespuesta del Pensador:\n{resultado_logico}\n")
    except Exception as e:
        print(f"\nFallback falló en el Pensador de Backend: {str(e)}\n")

if __name__ == "__main__":
    main()
