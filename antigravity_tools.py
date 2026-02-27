import os
import subprocess

# Adaptadores que exponen capacidades de Antigravity a PraisonAI
# En PraisonAI, cualquier función de Python puede pasarse como una herramienta.

def antigravity_read_file(filepath: str) -> str:
    """
    Lee el contenido completo de un archivo local.
    Útil para leer código, logs o configuraciones del sistema.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer el archivo {filepath}: {str(e)}"

def antigravity_write_file(filepath: str, content: str) -> str:
    """
    Escribe contenido en un archivo local. Si el archivo existe, lo sobreescribe.
    Útil para generar scripts, reportes o modificar configuraciones.
    """
    try:
        # Asegurar que el directorio exista
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Archivo escrito exitosamente en: {filepath}"
    except Exception as e:
        return f"Error al escribir en {filepath}: {str(e)}"

def antigravity_run_command(command: str) -> str:
    """
    Ejecuta un comando en la terminal local y devuelve su salida.
    (SEGURIDAD: Filtrar comandos destructivos en producción).
    """
    # [QA Seguridad] Bloqueamos comandos peligrosos básicos
    comandos_prohibidos = ["rm", "del", "format"]
    if any(cmd in command.lower() for cmd in comandos_prohibidos):
         return f"Seguridad: Comando rechazado por contener palabras bloqueadas."
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30 # [QA Seguridad] Timeout para evitar procesos zombis
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error de ejecución:\n{result.stderr}"
    except Exception as e:
        return f"Error crítico al ejecutar comando: {str(e)}"

def antigravity_phva_register_learning(id_err: str, plan: str, hacer: str, verificar: str, actuar: str) -> str:
    """
    Registra una lección aprendida en el archivo de troubleshooting y activa el re-entrenamiento del RAG.
    Usa este comando cuando soluciones un problema complejo para que otros agentes no repitan el error.
    """
    try:
        # Importamos la lógica localmente para evitar dependencias circulares si las hubiera
        from autotrain_phva import update_troubleshooting, trigger_rag_training
        
        if update_troubleshooting(id_err, plan, hacer, verificar, actuar):
            trigger_rag_training()
            return f"✅ PHVA {id_err} registrado y agentes re-entrenados con éxito."
        return "❌ Error al registrar el aprendizaje."
    except Exception as e:
        return f"Error en la rutina PHVA: {str(e)}"

# Lista de herramientas para exportar al agente
ANTIGRAVITY_TOOLS = [
    antigravity_read_file, 
    antigravity_write_file, 
    antigravity_run_command,
    antigravity_phva_register_learning
]
