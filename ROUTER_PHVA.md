# Memoria PHVA Vectorizada: Confiabilidad T1 (Router Aim)

**Estatus:** APRENDIENDO  
**Objetivo de Confiabilidad:** > 95% (Actual: 69.9%)

## 🧠 Patrones de Aprendizaje (Base de Conocimiento)

### 🧩 Patrón 001: Complejidad Lógica Excesiva
- **Detección**: Tareas de SQL avanzado o refactorización de múltiples archivos.
- **Fallo observado**: `gpt-4o-mini` tiende a alucinar o fallar en el uso de herramientas si el prompt excede los 2k tokens.
- **Regla T1**: Si el prompt > 2500 tokens en rol `logica`, escalar automáticamente a `Antigravity Pro` (GPT-4o).

### 🔍 Patrón 002: Búsqueda Profunda (Research)
- **Detección**: Consultas de mercado o datos técnicos de 2025/2026.
- **Fallo observado**: Modelos locales (Ollama) fallan por falta de conexión. Modelos Cloud genéricos fallan por falta de browsing.
- **Regla T1**: Forzar `Sonar (Perplexity)` para cualquier keyword que implique "tendencias", "precios actuales" o "última versión".

### ⚡ Patrón 003: Latencia y Timeouts
- **Detección**: Tareas de procesamiento de documentos largos (>10k tokens).
- **Fallo observado**: Timeout de 90s alcanzado en modelos lentos.
- **Regla T1**: Usar `Gemini Flash` exclusivamente para procesamiento masivo por su ventana de contexto y velocidad de respuesta.

## 🤖 Automatización de Aprendizaje (Rutina T1)
Para garantizar que el sistema nunca olvide lo aprendido, se ha implementado un flujo disparador:
1. **Registro**: Se inserta el hallazgo en `troubleshooting.md`.
2. **Entrenamiento**: Se invoca `autotrain_phva.py`.
3. **Consolidación**: El RAG local actualiza el vector store.

**Comando de Activación:**
`python autotrain_phva.py "[ID]" "[Plan]" "[Hacer]" "[Verificar]" "[Actuar]"`

---

## 📈 Histórico de Optimizaciones

| Fecha | Fallo Orig. | Acción Tomada | Impacto T1 |
| :--- | :--- | :--- | :--- |
| 2026-02-27 | 69.9% | Creación de Base PHVA | Inicio Linea Base |
| 2026-02-27 | 69.9% | Configuración RAG Local | Agentes con memoria semántica (Item 6) |

---
*Nota: Este archivo es consumido por el Router Agent antes de cada tarea.*
