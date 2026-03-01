---
name: self-evolution
description: >
  Automatiza la fase de "ACTUAR" del ciclo PHVA actualizando las instrucciones de las skills
  nativas basándose en el historial de errores y lecciones aprendidas.
  Usar cuando el usuario pida: evolucionar, auto-mejora, actualizar skills, mejorar infraestructura.
---

# 🧬 Self-Evolution: El Motor de Auto-Mejora de Antigravity

Esta skill dota a la terminal de la capacidad de aprender de sus propios errores de manera estructural. No solo resuelve el problema actual, sino que modifica su "ADN" (las instrucciones de las skills) para inmunizarse contra fallos recurrentes.

## El Ciclo de Evolución

### 1. Extracción de Patrones
Lee periódicamente (o a petición) la base de datos de troubleshooting en `skills/phva-cycle/troubleshooting/`.
- Busca IDs de error con frecuencia alta (más de 2 ocurrencias).
- Identifica la "Causa Raíz" y la "Solución" documentada.

### 2. Diagnóstico de Instrucciones
Identifica qué skill o mandato (`~/.gemini/antigravity/skills/` o prompts base) debería haber prevenido ese error.
- ¿Falta una regla en el `Mandato de Calidad Suprema`?
- ¿La skill de `test-fixing` no contempla este nuevo framework?
- ¿El `master-orchestrator` necesita un nuevo paso de verificación?

### 3. Propuesta de Mutación
Genera un bloque de `diff` para actualizar el archivo `SKILL.md` objetivo.
- **Acción:** Añadir una "Regla de Oro" o un paso prohibitivo.
- **Ejemplo:** Si el error es "olvido de centrar botones en mobile", la mutación añade a la skill de UI: *"Regla 9: TODO botón en viewport mobile inferior a 640px DEBE estar centrado horizontalmente por defecto."*

### 4. Revisión y Aplicación
Presenta la propuesta al usuario:
- *"He detectado que el error [ID] ha ocurrido 3 veces. Propongo actualizar la Skill [Nombre] con esta nueva directiva: [Descripción]. ¿Aplicamos la evolución?"*
- Tras la aprobación, usa la herramienta de edición para aplicar el cambio permanentemente.

## Disparadores (Triggers)
- **Manual:** "Analiza las lecciones aprendidas y evoluciona tus skills".
- **Automático:** Tras cerrar 5 proyectos exitosos con el `phva-cycle`.

## Regla de Seguridad
La auto-evolución **siempre** requiere aprobación humana. El agente no puede modificar sus directivas críticas sin el "OK" del usuario para evitar derivas de comportamiento inapropiadas.
