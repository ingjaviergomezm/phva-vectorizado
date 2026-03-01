# Corrective RAG (CRAG) Protocol — Antigravity

Este protocolo asegura que la información recuperada de nuestra memoria vectorial (o manuales) sea **relevante y útil** antes de ser procesada por el agente. Si la calidad es baja, el sistema se auto-corrige.

## Flujo de Evaluación de Relevancia

Después de realizar cualquier búsqueda en `skills/phva-cycle/troubleshooting/` o bases de datos externas:

### 1. Puntuación de Documentos (Scoring)
Evalúa cada documento/entrada recuperada en una escala de 0 a 10:
- **9-10 (Exacta):** El error y el framework coinciden plenamente. La solución es directamente aplicable.
- **6-8 (Relacionada):** El error es similar pero el framework o contexto varía ligeramente. Requiere adaptación.
- **0-5 (Irrelevante):** Ruido, información obsoleta o de un stack tecnológico no relacionado.

### 2. Decisiones de Acción
- **Relevancia Alta (> 8):** Procede con la solución documentada directamente.
- **Relevancia Media (6-8):** Utiliza la información como "pista", pero advierte al usuario o realiza una búsqueda de refinamiento.
- **Relevancia Baja (< 5):** **触发 TRIGGER CORRECTIVO.**

## Acciones Correctivas (The "C" in CRAG)

Si la relevancia es baja, el agente **NO DEBE** intentar adivinar. Debe ejecutar una de las siguientes:

1. **Refinamiento de Consulta:** Reformular la búsqueda usando términos técnicos más precisos extraídos de los logs de error reales.
2. **Búsqueda Web de Respaldo:** Si la memoria local falla, usar `search_web` para buscar soluciones en la comunidad (GitHub Issues, StackOverflow, Documentación oficial).
3. **Deep Research (Fallo Crítico):** Si el error es complejo y desconocido, invocar la skill `deep-research` para una investigación exhaustiva de 2-10 minutos.

## Ejemplo de Aplicación
> **Intento:** Busco error de "Tailwind v4 spacing".
> **Resultado:** Encuentro una entrada de "Tailwind v3 margin".
> **Score:** 4 (Relevancia Baja).
> **Acción CRAG:** Ignorar la entrada de v3. Ejecutar `search_web` buscando específicamente los cambios de breaking en la API de spacing de v4.
