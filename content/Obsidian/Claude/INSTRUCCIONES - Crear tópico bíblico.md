# Instrucciones para Cowork: Crear Tópico Bíblico

**Versión:** 1.0 (Marzo 2026)
**Autor:** Quique
**Propósito:** Documentar el proceso correcto para crear un nuevo tópico bíblico en el vault

---

## Contexto

Los tópicos bíblicos son notas de referencia teológica que agrupan sermones, meditaciones y citas relacionadas con un tema. Viven en `Biblioteca/02 Estudio/Temas bíblicos/` y están indexados en `Claude/Indice de temas biblicos.md`.

---

## Paso 1 — Verificar que no exista ya

Antes de crear el tópico, buscar en el índice si ya existe uno con ese nombre o uno equivalente:

```
Claude/Indice de temas biblicos.md
```

Si ya existe con otro nombre, usar ese nombre en lugar de crear un duplicado.

---

## Paso 2 — Identificar temas relacionados (related)

Abrir el índice y seleccionar entre **4 y 8 temas** que tengan relación directa con el nuevo tópico:

```
Claude/Indice de temas biblicos.md
```

**Reglas críticas:**
- Solo usar temas que **existan exactamente** en el índice (respetar capitalización y tildes)
- No inventar nombres de temas
- Si un tema importante no existe en el índice, **preguntar al usuario** si desea crearlo antes de continuar

---

## Paso 3 — Crear el archivo

**Ubicación:** `Biblioteca/02 Estudio/Temas bíblicos/[Nombre del tópico].md`

**Template:**

```markdown
---
type: TopicoBiblico
title: [Nombre del tópico]
parent: "[[Tópico padre si existe]]"
related:
  - "[[Tema relacionado 1]]"
  - "[[Tema relacionado 2]]"
  - "[[Tema relacionado 3]]"
tags:
  - TemasBiblicos
---


```dataview
table
FROM [[]]
SORT date DESC
` ``
```

**Notas sobre el frontmatter:**
- `parent`: tópico más amplio al que pertenece este tema (debe existir en el índice)
- `related`: solo temas del índice, verificados previamente
- No incluir campo `master` a menos que Quique lo indique
- Dejar una línea en blanco entre el cierre `---` y el bloque dataview

---

## Paso 4 — Actualizar el índice

Agregar el nuevo tópico en `Claude/Indice de temas biblicos.md` en **orden alfabético estricto**.

- Formato: `- [[Nombre del tópico]]`
- Verificar la letra inicial para ubicarlo correctamente entre los existentes

---

## Checklist final

- [ ] El nombre no duplica un tópico existente
- [ ] Todos los `related` existen en el índice
- [ ] El `parent` existe en el índice
- [ ] El archivo está en `Biblioteca/02 Estudio/Temas bíblicos/`
- [ ] El tópico fue agregado al índice en orden alfabético
