import os
from dotenv import load_dotenv
from praisonaiagents import Agent

# Importamos las herramientas (adaptadores) de Antigravity
from antigravity_tools import ANTIGRAVITY_TOOLS

# Cargar llaves desde .env
load_dotenv()

def main():
    # [Punto 4] Prompting específico para que el agente use las habilidades.
    # Usaremos gpt-4o-mini o gemini-1.5-flash asumiendo que ya configuraste la llave,
    # caso contrario, fallback a tu Ollama local (si ya tienes Llama 3 o Qwen instalados)
    
    # modelo = "ollama/qwen2.5:7b" # Descomenta para usar el local
    modelo = "gemini/gemini-flash-latest" # Default fallback de nube rápida

    vibe_coder_agent = Agent(
        name="AntigravityOperator",
        role="Vibe Coder Senior Engineer",
        goal="Interactuar con el sistema de archivos local y terminal para resolver peticiones complejas de configuración del usuario.",
        backstory="""Eres un experto ingeniero de desarrollo apoyado por el motor de Antigravity. 
Tienes acceso a herramientas para leer archivos, escribir archivos y ejecutar comandos en la terminal de Windows.
DEBES usar estas herramientas antes de adivinar o asumir datos locales.""",
        instructions="""Reglas estrictas (QA y Seguridad):
1. Si te piden información sobre el sistema, SIEMPRE usa `antigravity_run_command` primero (ej. `systeminfo` o `dir`).
2. Nunca asumas la existencia de carpetas; verifícalo lanzando comandos o leyendo con `antigravity_read_file`.
3. Informa al usuario exactamente el resultado de los comandos ejecutados.
4. Eres parte de un bucle de seguridad; si la consola lanza error, debes intentar arreglarlo con un nuevo comando sin detenerte.""",
        tools=ANTIGRAVITY_TOOLS,
        llm=modelo
    )

    print(f"=== Iniciando PraisonAI Vibe Coder (LLM: {modelo}) ===")
    print("El agente intentará descubrir información real de nuestro sistema...\n")

    # Tarea que obliga a usar las herramientas de Antigravity
    # Nota: praisonai 1.5.15 en Agent.start recibe string
    resultado = vibe_coder_agent.start(
        "Crea una carpeta llamada 'reportes_agente', luego crea un archivo dentro llamado 'specs.txt' donde listes el sistema operativo local usando un comando de consola. Léelo para confirmar que quedó bien y dime qué escribiste."
    )

    print("\n\n=== Resultado Final del Agente ===")
    print(resultado)

if __name__ == "__main__":
    main()
