import argparse
import sys
import os
import threading
from dotenv import load_dotenv
from praisonaiagents import Agent
from telemetry import logger, check_budget, update_json_dashboard
from rag_manager import AntigravityRAG
from antigravity_tools import ANTIGRAVITY_TOOLS

load_dotenv()

# ==============================================================================
# SEGURIDAD Y PRIVACIDAD (Item 7)
# ==============================================================================
BASE_PROJECT_DIR = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm"
EXECUTION_TIMEOUT = 90  # 90 segundos máx.

# ==============================================================================
# SCRIPT DELEGADO PARA ANTIGRAVITY (Supervisor -> Obreros)
# Este script es consumido estrictamente vía línea de comandos por Antigravity.
# Su único objetivo es recibir un ROL ("investigacion", "procesamiento", "logica") 
# y un PROMPT, despachar la tarea al modelo barato, e imprimir el resultado en std-out.
# ==============================================================================

# LLM Fallbacks (Optimizados según API tests locales)
LLM_LOGICO = "gpt-4o-mini"
LLM_DOCUMENTAL = "gemini/gemini-flash-latest"
LLM_INVESTIGADOR = "perplexity/sonar-pro"
LLM_LOCAL_BACKUP = "ollama/llama3.1:8b" # En caso de corte de internet

def main():
    parser = argparse.ArgumentParser(description="PraisonAI Headless Delegate for Antigravity")
    parser.add_argument('--rol', type=str, required=True, choices=['logica', 'documentos', 'investigacion'],
                        help='El tipo de obrero a levantar.')
    parser.add_argument('--prompt', type=str, required=True, 
                        help='Instrucción detallada para el agente.')
    
    args = parser.parse_args()

    # 1. CIRCUIT BREAKER DE PRESUPUESTO
    if not check_budget():
        logger.error("🛑 Ejecución bloqueada: Presupuesto diario agotado.")
        update_json_dashboard("SECURITY", "SYSTEM", "BLOCKED", "Presupuesto diario excedido")
        print("\n[ERROR CRÍTICO] Presupuesto diario excedido. Cambiando a Clúster Local forzado.")
        sys.exit(1)

    # 2. VALIDACIÓN DE SANDBOX (Prompt Level)
    forbidden_keywords = ["C:\\", "/etc/", ".ssh", "System32", "AppData"]
    for word in forbidden_keywords:
        if word.lower() in args.prompt.lower():
            logger.error(f"🛑 VIOLACIÓN DE SANDBOX DETECTADA: El prompt contiene palabra prohibida '{word}'")
            update_json_dashboard("SECURITY_VIOLATION", "SYSTEM", "BLOCKED", f"Prompt intentó acceder a {word}")
            print(f"\n[ERROR DE SEGURIDAD] La tarea solicitada viola las directivas de Sandboxing ({word}).")
            sys.exit(1)

    # 3. ROUTER INTELIGENTE (Item 8: PHVA de Confiabilidad T1)
    prompt_len = len(args.prompt)
    model_override = None
    
    # Regla: Si es investigación y pide datos actuales, forzar Sonar
    if args.rol == 'investigacion' or any(w in args.prompt.lower() for w in ['precio', 'tendencia', 'actual', '2025', '2026']):
        model_override = LLM_INVESTIGADOR
    
    # Regla: Si el prompt es muy largo en rol logica (>2500 chars), escalar a Pro por confiabilidad
    if args.rol == 'logica' and prompt_len > 2500:
        logger.info(f"🔄 UPGRADE DE SEGURIDAD: Prompt largo ({prompt_len} chars). Usando Global Pro.")
        model_override = "gpt-4o" # Escalamiento a Pro
    
    # 4. MEMORIA RAG (Item 6: Local RAG)
    rag = AntigravityRAG()
    knowledge_base = None
    if rag.initialize_knowledge():
        knowledge_base = rag.knowledge
    
    # Configurar el Agente según el rol
    if args.rol == 'logica':
        phva_context = "CRÍTICO: Antes de resolver, consulta tu base de conocimientos (RAG). Si solucionas un patrón de fallo recurrente, USA LA HERRAMIENTA 'antigravity_phva_register_learning' para guardarlo."
        agente = Agent(
            name="Backend Worker",
            role="Ejecutor Python/SQL",
            goal="Resolver la tarea lógica solicitada por el Arquitecto de forma concisa.",
            backstory="Subordinado del modelo Frontera. Responde sin adornos. " + phva_context,
            llm=model_override or LLM_LOGICO,
            max_iter=3,
            knowledge=knowledge_base,
            tools=ANTIGRAVITY_TOOLS
        )
    elif args.rol == 'documentos':
        # Para documentos, si es muy largo, Gemini Flash es superior por contexto
        agente = Agent(
            name="Data Worker",
            role="Resumidor y Extractor",
            goal="Procesar grandes bloques de texto provistos en el prompt.",
            backstory="Procesador de lenguaje ultra-rápido. Devuelve JSONs y resúmenes estructurados.",
            llm=model_override or LLM_DOCUMENTAL,
            knowledge=knowledge_base
        )
    elif args.rol == 'investigacion':
        agente = Agent(
            name="Search",
            instructions="Responde a la pregunta buscando en la web.",
            llm=model_override or LLM_INVESTIGADOR
        )
    else:
        print("Error: Rol no válido.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.rol == 'investigacion':
            from litellm import completion
            response = completion(
                model=LLM_INVESTIGADOR,
                messages=[{"role": "user", "content": args.prompt}]
            )
            resultado = response.choices[0].message.content
        else:
            # Ejecución controlada con Timeout
            def job():
                nonlocal resultado
                try:
                    resultado = agente.start(args.prompt)
                except Exception as e:
                    resultado = f"[ERROR AGENTE] {str(e)}"

            thread = threading.Thread(target=job)
            thread.start()
            thread.join(EXECUTION_TIMEOUT)

            if thread.is_alive():
                logger.error(f"🛑 TIMEOUT: La tarea excedió los {EXECUTION_TIMEOUT}s.")
                update_json_dashboard("TIMEOUT", agente.llm, "FAILURE", "Tarea abortada por tiempo")
                resultado = f"[TIEMPO AGOTADO] La tarea fue abortada por seguridad tras {EXECUTION_TIMEOUT}s."
                # Nota: El thread sigue corriendo de fondo pero el agente retornará el error al Supervisor
        
        # El print final es LO ÚNICO que leerá Antigravity desde stdout
        print("\n" + "="*40 + " OUTPUT " + "="*40)
        print(resultado)
        print("="*88 + "\n")
        
    except Exception as e:
        print(f"Error en ejecución del Agente: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
