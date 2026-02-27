# Base de Conocimiento de Troubleshooting (Ciclo PHVA)
*Este archivo sirve como memoria persistente para los agentes de PraisonAI y Antigravity. Antes de resolver un problema de código, el agente debe consultar este documento para evitar repetir errores conocidos.*

## 📋 Registro de Errores y Lecciones Aprendidas

### 001: Error de Sintaxis de LiteLLM al llamar a Perplexity API
**Planear:** Evitar que Perplexity arroje `litellm.BadRequestError: After the (optional) system message(s), user or tool message(s) should alternate with assistant message(s)`.
**Hacer:** Se removió el parámetro `backstory` en el agente de PraisonAI con LLM de Perplexity y se reemplazó la llamada usando `litellm.completion` directo.
**Verificar:** El error dejó de ocurrir y Perplexity pudo responder.
**Actuar:** REGLA: Nunca uses `backstory` o múltiples inyecciones de sistema con modelos de la familia Sonar (Perplexity). Usa strings directos en `user`.

---

### 002: Bloqueo de CORS y Desaparición de Datos (Dashboard HTML)
**Planear:** Resolver el escenario donde el Dashboard aparece vacío al refrescar (F5) o al ser abierto directamente desde el explorador de Windows (`file://`).
**Hacer:** 
1. Se identificó que los navegadores modernos bloquean peticiones `fetch()` a archivos locales por seguridad (CORS).
2. Se implementó un servidor web local en Python (`start_dashboard.py`).
3. Se creó un lanzador amigable (`.bat`) en el Escritorio para el usuario final.
4. Se unificaron las rutas de telemetría a rutas absolutas fijas para evitar inconsistencias de CWD (Current Working Directory).
**Verificar:** El dashboard carga consistentemente vía `http://localhost:8000` y sobrevive a refrescos de página y cambios de directorio de los agentes.
**Actuar:** REGLA: Nunca confíes en el protocolo `file://` para dashboards dinámicos. Siempre despliega un micro-servidor de archivos estáticos y usa rutas absolutas para la persistencia de datos JSON.

---
*(Antigravity Pro añadirá nuevas entradas aquí conformes los mini-agentes escalen bloqueos)*

---

### 004: Aprendizaje Automatizado PHVA
**Planear:** Automatización RAG
**Hacer:** Crear script autotrain_phva.py
**Verificar:** Agentes pueden auto-entrenarse
**Actuar:** REGLA: Siempre disparar entrenamiento tras cambios en memoria persistente
