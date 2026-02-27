import os
import json
from litellm import completion
from praisonaiagents import Agent
from telemetry import init_telemetry, logger, update_json_dashboard

# Inicializar Telemetría y Loggin Centralizados (Vacío 1)
init_telemetry()

# ==============================================================================
# 1. CONFIGURACIÓN DE LOS LLMs (Cloud First -> Local Backup) - Vacío 2
# ==============================================================================
# LiteLLM soporta listas de modelos para fallback automático.
# Formato: [Principal, Backup1, Backup2 (Local)]
LLM_LOGICO = ["gpt-4o-mini", "ollama/llama3.1:8b"]
LLM_DOCUMENTAL = ["gemini/gemini-flash-latest", "ollama/llama3.1:8b"]
LLM_INVESTIGADOR = ["perplexity/sonar-pro"] # Perplexity no tiene fallback local directo equivalente

# Enrutador rápido y barato para clasificar la intención
LLM_ROUTER_CLASSIFIER = ["gpt-4o-mini", "gemini/gemini-flash-latest"] 

# ==============================================================================
# 2. DEFINICIÓN DE LOS ASISTENTES ESPECIALIZADOS
# ==============================================================================

def get_agente_logico() -> Agent:
    return Agent(
        name="TechLead Agent",
        role="Ingeniero de Software y Arquitecto de Datos",
        goal="Escribir, auditar y depurar código, administrar bases de datos SQL y crear arquitecturas de software rigurosas.",
        backstory="Un ingeniero senior purista. Piensa estructuradamente y no comete errores de sintaxis.",
        instructions="Usa las herramientas asignadas paso a paso. Solo entrega código o análisis de bases de datos de alta calidad.",
        llm=LLM_LOGICO
    )

def get_agente_documental() -> Agent:
    return Agent(
        name="Data Processing Agent",
        role="Especialista en Documentos y Análisis de Contexto Largo",
        goal="Extraer datos precisos de documentos masivos y resumir bibliotecas corporativas enteras sin perder detalle.",
        backstory="Un bibliotecario analítico extremadamente meticuloso con memoria fotográfica.",
        instructions="Procesa exhaustivamente el texto. No omitas nombres importantes ni fechas clave en los resúmenes.",
        llm=LLM_DOCUMENTAL
    )

def get_agente_investigador() -> Agent:
    return Agent(
        name="Research Agent",
        role="Analista de Inteligencia Competitiva Web",
        goal="Navegar por la red, buscar fuentes recientes y confiables y cruzar datos en tiempo real.",
        backstory="Un investigador periodístico implacable con acceso directo al internet actual.",
        instructions="Usa motores de búsqueda en línea. Si das un dato cuantitativo, DEBES incluir la URL de la fuente.",
        llm=LLM_INVESTIGADOR
    )

# ==============================================================================
# 3. EL CEREBRO DEL ROUTER (Clasificador de Intenciones / Intent Classifier)
# ==============================================================================
def clasificar_tarea(prompt_usuario: str) -> str:
    """
    Usa el modelo más rápido de tu stack (OpenAI Mini) para entender si
    el usuario quiere programar, leer un archivo pesado o buscar en la web.
    """
    sistema_instrucciones = """
    Eres un Enrutador Maestro. Tu única tarea es leer lo que pide el usuario y 
    responder ÚNICAMENTE con una de las siguientes tres palabras, sin comillas ni puntos:
    - LOGICA (si implica programar, resolver matemáticas, usar SQL o analizar arquitectura).
    - DOCUMENTOS (si implica leer o resumir un PDF, un Word, correos o hacer RAG interno).
    - INVESTIGACION (si implica buscar datos de mercado actuales en internet, noticias o negocios actuales).
    """
    
    try:
        response = completion(
            model=LLM_ROUTER_CLASSIFIER[0], # Primer modelo
            fallbacks=LLM_ROUTER_CLASSIFIER[1:], # Resto como fallbacks
            messages=[
                {"role": "system", "content": sistema_instrucciones},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        return response.choices[0].message.content.strip().upper()
    except Exception as e:
        logger.error(f"[ROUTER ERROR] Fallo en clasificación: {str(e)}. Fallback a LOGICA.")
        return "LOGICA"

# ==============================================================================
# 4. ORQUESTADOR MAESTRO
# ==============================================================================
def despachar_y_ejecutar(prompt_usuario: str):
    logger.info(f"--- Nueva Petición Recibida: '{prompt_usuario}' ---")
    
    intencion = clasificar_tarea(prompt_usuario)
    logger.info(f"Categoría Detectada -> {intencion}")
    
    # Derivación al Agente Especialista
    if intencion == "INVESTIGACION":
        agente = get_agente_investigador()
    elif intencion == "DOCUMENTOS":
        agente = get_agente_documental()
    else:  # LOGICA o fallback
        agente = get_agente_logico()
        
    logger.info(f"Despachando a Agente: {agente.name} (Lista LLM: {agente.llm})")
    
    # Ejecutando la labor en PraisonAI con MANEJO DE ERRORES Y FALLBACK MANUAL - Vacío 2
    modelos_a_probar = agente.llm if isinstance(agente.llm, list) else [agente.llm]
    exito = False
    
    for modelo in modelos_a_probar:
        try:
            logger.info(f"[PROBANDO MODELO] {modelo} para el agente {agente.name}")
            agente.llm = modelo # Forzamos el modelo actual para este intento
            print(f"\n[Router] Intentando con {agente.name} (Modo: {modelo})...")
            
            respuesta = agente.start(prompt_usuario)
            
            print("\n=== RESPUESTA FINAL ===")
            print(respuesta)
            print("========================\n")
            exito = True
            break # Salimos del bucle si tuvo éxito
            
        except Exception as e:
            err_msg = str(e)[:100]
            logger.warning(f"[FALLBACK TRIGGERED] Modelo {modelo} falló. Error: {err_msg}")
            
            # Registrar el evento de Fallback en el Dashboard
            update_json_dashboard(
                event_type="FALLBACK", 
                model=modelo, 
                status="RECOVERED", 
                message=f"Fallo en {modelo}. Conmutando...",
                cost=0.0,
                pro_cost=0.0,
                latency=0.0
            )
            continue # Intentamos el siguiente modelo en la lista
            
    if not exito:
        error_msg = f"CRITICO: El agente {agente.name} falló incluso tras agotar TODA la lista de fallbacks: {modelos_a_probar}"
        logger.critical(error_msg)
        print(f"\n[ERROR] No se pudo completar la tarea tras múltiples reintentos. Revisa telemetría.\n")


if __name__ == "__main__":
    print("\n" + "#" * 60)
    print("SISTEMA ANTIGRAVITY v2: ROUTING + TELEMETRÍA + FALLBACK")
    print("#" * 60)
    
    # 1. Tarea matemática / código
    despachar_y_ejecutar("Escribe una consulta SQL para hallar el segundo empleado mejor pagado.")
    
    # 2. Tarea de resumen
    despachar_y_ejecutar("Tengo un acta notarial gigantesca de 500 páginas. Haz un resumen ejecutivo.")
    
    # 3. Tarea de Web Search Actual
    despachar_y_ejecutar("Busca y dime cuál es el precio actual de la acción de Apple hoy.")
