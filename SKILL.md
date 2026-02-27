---
name: phva-cycle
description: >
  Ciclo PHVA (Planear-Hacer-Verificar-Actuar) de mejora continua. Activar
  SIEMPRE antes de entregar cualquier trabajo de frontend, UI/UX, maquetado,
  o cualquier tarea donde se hayan cometido errores recurrentes documentados
  en las lecciones aprendidas. También activar cuando el usuario mencione:
  ciclo PHVA, mejora continua, calidad, lecciones aprendidas, no repetir errores.
---

# 🔄 Ciclo PHVA — Sistema de Mejora Continua Antigravity

## Propósito

Este skill existe porque **desperdiciamos tokens y tiempo del usuario corrigiendo errores
repetitivos**. Cada iteración innecesaria cuesta dinero, tiempo y confianza.

El sistema opera en **dos modos** y mantiene una **base de datos de troubleshooting**
persistente e indexada.

> "Lo que no se mide no se mejora, y lo que no se documenta se repite." — Adaptado de Deming

---

## 🎯 ACTIVACIÓN AUTOMÁTICA

### Modo 1: RETROSPECTIVA (Post-proyecto)

**Se activa cuando el usuario dice:**
- "Ya quedó listo"
- "Voy a publicarlo"
- "Deploy", "push a producción", "subir a GitHub"
- "El proyecto está terminado"
- "Vamos a cerrar este proyecto"
- Cualquier variación que indique que el proyecto llegó a su versión final.

**Acción:** Ejecutar el proceso de Retrospectiva (sección "ACTUAR — Retrospectiva").

### Modo 2: CONSULTA PROACTIVA (Durante desarrollo)

**Se activa automáticamente cuando:**
- Un error de CSS/spacing/layout se presenta y no se resuelve en el primer intento.
- El usuario reporta un defecto visual (texto invisible, solapamiento, desbordamiento).
- Se está trabajando con un framework CSS y hay dudas sobre compatibilidad.
- Un error parece familiar o ya documentado.

**Acción:** ANTES de intentar solucionar, consultar la base de datos de troubleshooting
en `skills/phva-cycle/troubleshooting/` para ver si ya hay una solución documentada.

---

## 📋 PROTOCOLO PHVA

### P — PLANEAR (Antes de escribir código)

1. **Verificar el stack tecnológico:**
   - ¿Qué versión de Tailwind/CSS framework usa el proyecto? (`package.json`)
   - ¿Hay un `tailwind.config` con extensiones custom?
   - ¿El proyecto usa dark mode? ¿Cuál es el tema activo del usuario?

2. **Definir la jerarquía tipográfica (si aplica UI):**
   - ¿Cuál es el H1 de la página? (Solo 1 por página)
   - ¿Cuáles son los H2? (Títulos de sección)
   - ¿Cuáles son los H3? (Subtítulos)
   - ¿El texto va centrado, izquierdo, o justificado?

3. **Consultar troubleshooting:**
   - Leer `skills/phva-cycle/troubleshooting/index.md` para buscar errores conocidos
     que apliquen al contexto actual (mismo framework, mismo tipo de componente).
   - Si hay match, aplicar la solución documentada directamente.

4. **Confirmar con el usuario** si hay ambigüedad.

### H — HACER (Implementación)

1. Escribir el código siguiendo el plan.
2. Aplicar soluciones de troubleshooting conocidas de forma preventiva.
3. Respetar semántica HTML para componentes visuales.

### V — VERIFICAR (Antes de entregar)

**⚠️ OBLIGATORIO. NUNCA SALTAR. ⚠️**

1. **Abrir el browser** y tomar capturas de pantalla REALES.
2. **Revisar CADA captura personalmente** (NO confiar en reportes textuales del subagent).
3. **Checklist de verificación visual:**
   - [ ] Jerarquía tipográfica correcta (H1 > H2 > H3)
   - [ ] Centrado/alineación según requerimiento
   - [ ] Spacing visible entre TODAS las secciones
   - [ ] Funciona en light mode Y dark mode
   - [ ] Videos/imágenes no dominan el viewport
   - [ ] Contraste de texto suficiente
4. **Inspeccionar CSS con JavaScript** si el spacing no aplica:
   ```javascript
   const el = document.querySelector('section');
   console.log(getComputedStyle(el).marginBottom);
   ```
5. Si CUALQUIER punto falla → **corregir ANTES de responder**.

### A — ACTUAR (Retrospectiva y Documentación)

**Se ejecuta cuando el usuario indica que el proyecto está listo para publicar.**

#### Proceso de Retrospectiva:

1. **Analizar la conversación** e identificar todos los errores que ocurrieron:
   - ¿Cuántas iteraciones tomó cada corrección?
   - ¿Cuáles fueron errores evitables?
   - ¿Cuáles fueron errores de primera vez (nuevos)?

2. **Clasificar cada error** según las categorías del index de troubleshooting.

3. **Documentar errores nuevos** en la base de datos:
   - Crear un archivo `.md` por cada error en `troubleshooting/entries/`
   - Actualizar `troubleshooting/index.md` con la referencia

4. **Reportar al usuario** un resumen:
   ```
   📊 Retrospectiva PHVA — [Nombre del Proyecto]
   ├── Errores totales: X
   ├── Errores evitables (ya documentados): Y
   ├── Errores nuevos documentados: Z
   ├── Tokens estimados desperdiciados: [bajo/medio/alto]
   └── Nuevas entradas en troubleshooting: [lista]
   ```

5. **Actualizar las métricas** en `troubleshooting/metrics.md`.

---

## 🗃️ BASE DE DATOS DE TROUBLESHOOTING

### Estructura de archivos

```
skills/phva-cycle/
├── SKILL.md                          ← Este archivo
└── troubleshooting/
    ├── index.md                      ← Índice maestro (búsqueda rápida)
    ├── metrics.md                    ← Métricas históricas
    └── entries/
        ├── CSS-001-tailwind-v4-spacing.md
        ├── CSS-002-dark-light-contrast.md
        ├── UI-001-typography-hierarchy.md
        ├── QA-001-subagent-hallucination.md
        └── ...
```

### Formato de cada entrada

Cada archivo en `entries/` sigue este formato:

```markdown
# [ID] — [Título corto]
- **Categoría:** CSS | UI | QA | JS | API | Config | Performance
- **Framework:** Tailwind v4 | React | Vite | General
- **Severidad:** 🔴 Crítica | 🟡 Media | 🟢 Baja
- **Tokens desperdiciados:** Alto | Medio | Bajo
- **Proyecto origen:** [Nombre]
- **Fecha:** [YYYY-MM-DD]

## Síntomas
[¿Qué ve el usuario? ¿Qué reporta?]

## Causa Raíz
[¿Por qué ocurrió realmente?]

## Solución
[Pasos exactos para resolver]

## Prevención
[¿Cómo evitarlo en el futuro?]
```

### Consulta rápida

Cuando se detecta un error durante el desarrollo:

1. Leer `troubleshooting/index.md`
2. Buscar por **categoría** + **síntoma**
3. Si hay match → leer la entrada completa → aplicar solución
4. Si no hay match → resolver y DOCUMENTAR como nueva entrada

---

## 🚨 REGLAS DE ORO

1. **NUNCA entregar frontend sin verificación visual propia**
2. **SIEMPRE verificar la versión del framework CSS antes de usar clases**
3. **NUNCA confiar ciegamente en reportes textuales del browser subagent**
4. **SIEMPRE definir jerarquía H1/H2/H3 antes de codificar**
5. **SIEMPRE probar en AMBOS temas (light + dark)**
6. **Si una clase CSS no aplica, usar `getComputedStyle()` inmediatamente**
7. **Ante un error: PRIMERO consultar troubleshooting, DESPUÉS intentar solucionar**
8. **Al cierre de proyecto: SIEMPRE ejecutar retrospectiva PHVA**
