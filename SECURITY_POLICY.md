# Directivas de Seguridad y Privacidad: Antigravity Hybrid Engine

**Estatus:** ACTIVO  
**Versión:** 1.0 (Feb 2026)

## 🛡️ 1. Política de Aislamiento (Sandboxing)
Los agentes delegados (PraisonAI Workers) operan bajo un modelo de "Confianza Cero" respecto al sistema anfitrión.

- **Espacio de Trabajo Único**: Solo se permite la lectura y escritura dentro del directorio `scratch/ingjaviergomezm/`.  
- **Prohibición de Acceso OS**: Los agentes no tienen permiso para ejecutar comandos que afecten el registro de Windows, configuraciones de red o archivos de usuario fuera de la zona de scratch.  
- **Aislamiento de Procesos**: Cada tarea de obrero se lanza como un proceso independiente con un tiempo de vida (TTL) limitado.

## 🔐 2. Clasificación y Privacidad de Datos
El enrutamiento de datos se rige por la siguiente matriz de sensibilidad:

| Nivel | Descripción | Enrutador Permitido | Ejemplo |
| :--- | :--- | :--- | :--- |
| **PÚBLICO** | Información disponible en la web. | Cloud (Global) | Scraping, Research, Tendencias. |
| **SENSIBLE** | Datos del proyecto, estructura de código. | Cloud (Enmascarados) | Refactorización, Análisis de KPIs. |
| **CRÍTICO** | Credenciales, datos financieros privados, IP. | **LOCAL ONLY** (Ollama) | Manejo de .env, Llaves de API, Costos. |

**Regla de Oro**: Ningún dato marcado como *CRÍTICO* debe ser enviado a un endpoint de API externo (OpenAI, Anthropic, Google).

## ⏳ 3. Límites de Ejecución (Circuit Breakers)
- **Iteraciones Max (max_iter)**: 3. Si el agente no resuelve en 3 intentos, escala al Supervisor Pro.
- **Tiempo Límite (Timeout)**: 90 segundos por tarea.
- **Límite de Presupuesto Diario**: $2.00 USD. Al alcanzarlo, el sistema bloquea el enrutamiento a Cloud y fuerza el uso del Clúster Local.

## 📝 4. Auditoría
Todas las violaciones a estas políticas (intentos de acceso fuera del sandbox o exceso de límites) se registran en `history_metrics.json` con el estado `SECURITY_VIOLATION`.

---
*Firma: Arquitecto Supervisor Antigravity*
