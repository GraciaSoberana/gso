# Instrucciones para organizar Credos y Confesiones en Obsidian

Este documento describe el flujo de trabajo completo para estructurar credos, catecismos y confesiones de fe en el vault, siguiendo el modelo establecido con el Catecismo de Heidelberg (1563).

---

## Estructura de carpetas

```
Credos y confesiones/
└── [Nombre del documento]/
    ├── [Nombre del documento].md        ← Nota índice principal
    ├── [imagen].png                     ← Banner (opcional)
    ├── 01. [Título de la pregunta/artículo].md
    ├── 02. [Título de la pregunta/artículo].md
    └── ...
```

---

## Formato de la nota índice principal

```yaml
---
type: ChurchHistory
class: creed
title: [Nombre del documento]
year: "[año]"
master: "[[Historia de la Iglesia]]"
periodo: "[[Reforma protestante]]"   ← o el período correspondiente
parent: "[[Credos y confesiones]]"
related:
tags:
  - HistoriaIglesia/Catecismo
---
![[imagen.png|banner]]

### Sección 1 (ej. Día del Señor 1)

1. [[01. Título de la pregunta|¿Texto completo de la pregunta?]]
2. [[02. Título de la pregunta|¿Texto completo de la pregunta?]]

### Sección 2
...
```

La nota índice actúa exclusivamente como tabla de contenidos con wiki links. No debe contener el texto de las respuestas.

---

## Formato de cada nota individual (pregunta/artículo)

```yaml
---
type: ChurchHistory
class: CreedArticle
sequence: [número]
aliases:
  - "¿Texto completo de la pregunta?"
title: "¿Texto completo de la pregunta?"
year: "[año]"
master: "[[Historia de la Iglesia]]"
periodo: "[[Reforma protestante]]"
parent: "[[Nombre del documento]]"
related:
  - "[[Tópico 1]]"
  - "[[Tópico 2]]"
  - "[[Tópico 3]]"
  - "[[Tópico 4]]"
tags:
  - HistoriaIglesia/Catecismo
---
![[imagen.png|banner]]

[Texto completo de la respuesta]
```

### Convención de nombres de archivo

- Formato: `[número]. [Texto de la pregunta sin ¿ ni ?].md`
- Números 1–9: con cero inicial → `01.`, `02.`, etc.
- Números 10–99: sin cero → `10.`, `11.`, etc.
- Números 100+: sin padding → `100.`, `101.`, etc.
- El título en el nombre del archivo es el texto de la pregunta tal cual, sin signos de interrogación.

---

## Flujo de trabajo paso a paso

### Paso 1 — Análisis inicial
Antes de comenzar, pedir a Claude que analice el documento y confirme:
- Número total de preguntas/artículos
- Estructura de secciones (partes, capítulos, días del Señor, etc.)
- Cuáles ya existen como notas individuales y cuáles faltan

### Paso 2 — Creación de notas individuales
Para cada pregunta/artículo que no tenga nota propia:
- Crear el archivo con el frontmatter completo
- Incluir el texto de la respuesta tal como aparece en el documento
- Asignar tópicos en el campo `related` (4 por nota, tomados del índice de temas bíblicos)

### Paso 3 — Actualización del índice principal
Reemplazar cualquier contenido en línea (respuestas pegadas directamente) por wiki links con el formato:
```
- [[Nombre del archivo|Texto visible de la pregunta]]
```

### Paso 4 — Revisión de tópicos `related`
Comparar cada tópico usado contra el `Indice de temas biblicos.md` y clasificarlos en:

- **Coincidencia exacta** → usar tal cual
- **Coincidencia cercana** → reemplazar por el nombre exacto del índice (el índice gobierna)
- **Sin equivalente** → crear nueva nota de tópico bíblico

### Paso 5 — Corrección masiva de tópicos cercanos
Hacer las sustituciones en todos los archivos de la carpeta de una sola vez. Ejemplos frecuentes:
- `[[Santa Cena]]` → `[[Cena del Señor]]`
- `[[Evangelio]]` → `[[El evangelio]]`
- `[[Bautismo]]` → `[[El bautismo]]`
- `[[Sacramentos]]` → `[[Los sacramentos]]`
- Revisar siempre el índice actualizado antes de hacer las sustituciones

### Paso 6 — Creación de nuevos tópicos bíblicos
Para cada tópico sin equivalente, crear una nota en `topicos biblicos/` con este formato:

```yaml
---
type: TopicoBiblico
title: [Nombre del tópico]
parent: "[[Tópico relacionado más cercano del índice]]"
related:
  - "[[Tópico relacionado 1]]"
  - "[[Tópico relacionado 2]]"
  - "[[Tópico relacionado 3]]"
  - "[[Tópico relacionado 4]]"
tags:
  - TemasBiblicos
master: "[[Master topic]]"
---

# [Nombre del tópico]

## Definición
[Definición teológica concisa, 3-5 oraciones]

## Características bíblicas
- [Característica 1]
- [Característica 2]
- [Característica 3]
- [Característica 4]
- [Característica 5]

## Pasajes clave
- [[Referencia]] — Descripción breve
- [[Referencia]] — Descripción breve
- [[Referencia]] — Descripción breve
- [[Referencia]] — Descripción breve
```

El campo `master` debe ser uno de los master topics del índice:
`[[Biblia]]`, `[[Cristo]]`, `[[Dios padre]]`, `[[Escatología]]`, `[[Espíritu Santo]]`, `[[Familia cristiana]]`, `[[Iglesia]]`, `[[Pecado]]`, `[[Salvación]]`, `[[Santificación]]`, `[[Teología bíblica]]`, `[[Teología práctica]]`, `[[Ética y cultura]]`

### Paso 7 — Actualización del índice de temas bíblicos
Añadir todas las nuevas notas de tópicos al `Indice de temas biblicos.md`, en la sección `### Temas biblicos actuales:`, antes de `### Masters:`.

---

## Reglas importantes

1. **El índice gobierna**: si un tópico existe en el `Indice de temas biblicos.md`, debe usarse con ese nombre exacto, sin variaciones.
2. **4 tópicos por nota**: el campo `related` de cada nota individual debe tener exactamente 4 entradas.
3. **No mezclar contenido e índice**: la nota principal solo tiene wiki links, nunca el texto de las respuestas.
4. **Consistencia tipográfica**: los nombres de archivo no llevan `¿` ni `?`; el `title` y `aliases` sí los llevan.
5. **Un archivo por pregunta**: aunque la nota índice agrupe varias preguntas bajo un "Día del Señor" o sección, cada pregunta es su propio archivo.

---

## Información de contexto útil para proporcionar a Claude

Al iniciar un nuevo proyecto de este tipo, compartir con Claude:
- El archivo del documento a estructurar (o su texto)
- La carpeta destino dentro de `Credos y confesiones/`
- El nombre de la imagen banner (si existe)
- El período histórico (Reforma, Patrística, Medieval, etc.)
- Cuántas notas ya existen, si es un trabajo parcial
- El archivo `Indice de temas biblicos.md` (o confirmar que Claude ya tiene acceso)

---

## Documentos candidatos para el mismo tratamiento

- Confesión de Fe de Westminster (1646) — 33 capítulos
- Catecismo Mayor de Westminster (1648) — 196 preguntas
- Catecismo Menor de Westminster (1647) — 107 preguntas
- Confesión Belga (1561) — 37 artículos
- Cánones de Dort (1618-1619) — 5 capítulos
- Segunda Confesión Helvética (1566)
- Catecismo de Lutero (Mayor y Menor, 1529)
- Artículos de Religión (39 artículos anglicanos, 1563)

---

*Generado a partir del trabajo realizado con el Catecismo de Heidelberg — marzo 2026*
