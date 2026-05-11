# Guía de Corrección: Series Apocalipsis

## Cambios necesarios

### Estructura de metadatos:
- ❌ `passage:` → ✅ `mainpassage:`
- ❌ Formato variable → ✅ `[[Ap. X]]` (con punto)
- ✅ Agregar `otherpassages:` si hay múltiples pasajes
- ✅ Normalizar `related:` con temas del Indice
- ✅ Formato de fecha: YYYY-MM-DD → YYYY-MM-DDTHH:MM (usar 12:00)
- ✅ Normalizar `tags:` a todos (incluir `- Sermones`)
- ✅ Agregar `pdg:` vacío al final

---

## Mapeo de correcciones por archivo

---

## Otros campos (consistentes en todos):
- `preacher:` → `[[Quique]]` (ya está correcto)
- `series:` → `[[Apocalipsis - La victoria del Cordero]]` (ya está correcto)
- `audience:` → `[[Gracia Soberana Orizaba]]` (ya está correcto)
- `tags:` → `- Sermones` (agregar/normalizar)
- `date:` → Convertir a `YYYY-MM-DDTHH:MM` (agregar T12:00)
- `slides:` → Mantener como está (campo adicional)
- `audio:` → Mantener como está (campo adicional)
- `pdg:` → Agregar vacío al final

---

## Orden correcto de campos en frontmatter:
```yaml
---
type: sermon
mainpassage: "[[Ap. X]]"
otherpassages:
* "[[Ap. Y]]"
series: "[[Apocalipsis - La victoria del Cordero]]"
related:
  - "[[Tema 1]]"
  - "[[Tema 2]]"
sequence: #
preacher: "[[Quique]]"
date: YYYY-MM-DDTHH:MM
tags:
  - Sermones
audience: "[[Gracia Soberana Orizaba]]"
pdg:
---
```
