---
description: Registra una nueva lección en troubleshooting.md y re-entrena el RAG local automáticamente.
---

Este flujo de trabajo automatiza el ciclo PHVA de aprendizaje del sistema.

### Pasos:

1. **Recopilación**: Define el Planear, Hacer, Verificar y Actuar de la lección.
2. **Ejecución de Rutina**:
// turbo
3. Ejecuta el comando: `python autotrain_phva.py "[ID]" "[Plan]" "[Hacer]" "[Verificar]" "[Actuar]"`

### Ejemplo de uso:
`python autotrain_phva.py "003" "Evitar alucinaciones en SQL" "Añadir esquemas previos" "Tests pasaron al 100%" "REGLA: Siempre leer el schema DDL antes de generar queries"`
