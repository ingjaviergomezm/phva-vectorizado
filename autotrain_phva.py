import os
import sys
import subprocess
from datetime import datetime
from telemetry import logger, update_json_dashboard

def update_troubleshooting(id_err, planear, hacer, verificar, actuar):
    """
    Actualiza el archivo troubleshooting.md con una nueva lección aprendida.
    """
    file_path = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm\troubleshooting.md"
    
    new_entry = f"""
---

### {id_err}: Aprendizaje Automatizado PHVA
**Planear:** {planear}
**Hacer:** {hacer}
**Verificar:** {verificar}
**Actuar:** {actuar}
"""
    
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(new_entry)
        logger.info(f"✅ Nueva entrada añadida a troubleshooting.md: {id_err}")
        return True
    except Exception as e:
        logger.error(f"❌ Error al escribir en troubleshooting.md: {e}")
        return False

def trigger_rag_training():
    """
    Ejecuta el script de re-entrenamiento RAG.
    """
    train_script = r"C:\Users\Usuario\.gemini\antigravity\scratch\ingjaviergomezm\train_agents_rag.py"
    try:
        logger.info("🔄 Iniciando re-entrenamiento RAG post-registro...")
        result = subprocess.run([sys.executable, train_script], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info("✅ Re-entrenamiento completado con éxito.")
            print(result.stdout)
            return True
        else:
            logger.error(f"❌ Fallo en re-entrenamiento: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ Error al ejecutar train_agents_rag.py: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python autotrain_phva.py 'ID' 'Plan' 'Hacer' 'Verificar' 'Actuar'")
        sys.exit(1)
        
    id_val = sys.argv[1]
    plan = sys.argv[2]
    hace = sys.argv[3]
    veri = sys.argv[4]
    actu = sys.argv[5]
    
    if update_troubleshooting(id_val, plan, hace, veri, actu):
        trigger_rag_training()
        update_json_dashboard(
            event_type="PHVA_AUTO_UPDATE",
            model="Antigravity Routine",
            status="SUCCESS",
            message=f"PHVA {id_val} registrado y re-entrenado.",
            cost=0.0,
            pro_cost=5.0,
            latency=0.0
        )
