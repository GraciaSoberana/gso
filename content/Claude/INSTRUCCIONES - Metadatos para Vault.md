# Instrucciones: Frontmatter y Metadatos para el Vault

**Versión:** 2.3 (Actualizado Feb 2026)
**Autor:** Quique
**Propósito:** Documentar el sistema de metadatos YAML para mantener consistencia en diferentes tipos de contenido

---

## 📋 Tabla de Contenidos
1. [Estructura General del Frontmatter](#estructura-general)
2. [Campos Disponibles](#campos-disponibles)
3. [Tipos de Contenido](#tipos-de-contenido)
4. [Índices de Referencia](#índices-de-referencia)
5. [Notas sobre Evolución](#notas-sobre-evolución)
6. [Checklist de Revisión](#checklist-de-revisión)
7. [Banners de serie](#banners)
8. [Manejo de Tópicos Bíblicos Faltantes](#topicos-faltantes)

---

## Estructura General del Frontmatter {#estructura-general}

Todos los archivos de contenido deben comenzar con frontmatter YAML encerrado entre `---`. Este es el formato **actual** (Feb 2026):

```yaml
---
type: [tipo de contenido]
mainpassage: "[[Referencia Bíblica]]"
otherpassages:
* "[[Ref 1]]"
* "[[Ref 2]]"
series: "[[Nombre de Serie]]"
related:
  - "[[Tema Bíblico 1]]"
  - "[[Tema Bíblico 2]]"
sequence: [número]
preacher: "[[Nombre]]"
date: YYYY-MM-DDTHH:MM
tags:
  - TagPrincipal
  - Tag/Secundario
audience: "[[Audiencia/Iglesia]]"
pdg:
---
```

**Orden de campos:** Importante mantener este orden para consistencia.

---

## Campos Disponibles {#campos-disponibles}

| Campo | Descripción | Requerido | Formato | Notas |
|-------|-------------|-----------|---------|-------|
| `type` | Tipo de contenido | ✅ | `sermon`, `meditacion`, `cita`, `topico` | Determina el tipo de contenido |
| `topic` | Tema central del sermón temático | ⚠️ | `[[Nombre del tópico]]` | Solo en sermones temáticos; va antes de `mainpassage` |
| `mainpassage` | Pasaje bíblico principal | ✅ | `[[Libro Cap]]` ej: `[[2 Tim 3]]` | Vacío en sermones temáticos; usar índice_biblia.md |
| `otherpassages` | Pasajes secundarios citados | ⚠️ | Lista con `* "[[Ref]]"` | Opcional; importante para sermones |
| `series` | Nombre de la serie (si aplica) | ⚠️ | `[[Nombre Serie]]` | Deja vacío si no es parte de una serie |
| `related` | Temas bíblicos conectados | ✅ | Lista con `  - "[[Tema]]"` | Usar Indice de temas biblicos.md |
| `sequence` | Orden dentro de la serie | ⚠️ | Número entero | Solo si es parte de serie |
| `preacher` | Persona que predicó/escribió | ✅ | `[[Nombre]]` | Para sermones, generalmente "[[Quique]]" |
| `date` | Fecha de predicación/creación | ✅ | `YYYY-MM-DDTHH:MM` | ej: `2023-01-29T12:00` |
| `tags` | Etiquetas de categorización | ✅ | Lista YAML | `- Sermones`, `- Meditaciones`, etc. |
| `audience` | Audiencia/iglesia/contexto | ✅ | `[[Nombre Iglesia]]` | ej: `[[Gracia Soberana Orizaba]]` |
| `pdg` | Hojas de trabajo grupos pequeños | ⚠️ | `[[Archivo PDG]]` o vacío | Nuevas PDG pueden ir aquí o como links en el contenido |

**Leyenda:** ✅ = Siempre requerido | ⚠️ = Condicional/Opcional según tipo

---

## Tipos de Contenido {#tipos-de-contenido}

### 1️⃣ SERMON (type: sermon)

**Descripción:** Mensaje predicado en una iglesia/evento. Existen dos variantes:

#### 1a. Sermón expositivo
Expone un pasaje bíblico específico. Usa `mainpassage` con el pasaje principal.

**Ejemplo:**
```yaml
---
type: sermon
mainpassage: "[[2 Tim 2]]"
otherpassages:
* "[[Mat 16]]"
* "[[1 Cor 2]]"
series: "[[Firmes en el legado del evangelio]]"
related:
  - "[[Gracia]]"
  - "[[El evangelio]]"
  - "[[Sufrimiento]]"
  - "[[Discipulado]]"
sequence: 1
preacher: "[[Quique]]"
date: 2023-01-29T12:00
tags:
  - Sermones
audience: "[[Gracia Soberana Orizaba]]"
pdg:
---
```

#### 1b. Sermón temático
Desarrolla un tema teológico sin un pasaje expositivo único. Usa `topic:` en lugar de `mainpassage:`. El `mainpassage:` queda vacío.

**Reglas:**
- `topic:` va **antes** de `mainpassage:` en el frontmatter
- `topic:` referencia un tópico bíblico o nota de estudio (`[[Nombre del tema]]`)
- `mainpassage:` se deja vacío — no forzar un pasaje ancla
- `related:` solo contiene tópicos del índice (no repetir el `topic:`)
- `otherpassages:` se puede poblar con los pasajes más citados en el sermón

**Ejemplo:**
```yaml
---
type: sermon
topic: "[[La persona y la obra del Espíritu Santo]]"
mainpassage:
otherpassages:
series: "[[Una vida guiada por el Espíritu Santo]]"
related:
  - "[[Espíritu Santo]]"
  - "[[Llenura del Espíritu Santo]]"
  - "[[Santificación]]"
sequence: 5
preacher: "[[Quique]]"
date: 2025-04-13T10:00
tags:
  - Sermones
audience: "[[Gracia Soberana Orizaba]]"
pdg:
---
```

---

### 2️⃣ MEDITACION (type: meditacion)

**Descripción:** Meditación/reflexión en un versículo o pasaje corto. Típicamente devocional o personal.

**Campos obligatorios:**
- `type: meditacion`
- `mainpassage` — el versículo/pasaje meditado
- `otherpassages` — pasajes conexos (opcional pero recomendado)
- `series` — si es parte de una serie de meditaciones (ej: "Meditaciones en Salmos")
- `date` — cuándo fue escrita/meditada
- `tags` — incluir `Meditaciones`
- `related` — temas que emergen de la meditación
- **No** necesita: `sequence`, `preacher`, `audience`, `pdg`

**Ejemplo:**
```yaml
---
type: meditacion
mainpassage: "[[Sal 23]]"
otherpassages:
* "[[Juan 10]]"
* "[[1 Pet 5]]"
series: "[[Meditaciones en Salmos]]"
related:
  - "[[Cristo como Pastor]]"
  - "[[Confianza en Dios]]"
  - "[[Protección de Dios]]"
  - "[[Paz de Dios]]"
date: 2025-06-15T07:00
tags:
  - Meditaciones
  - Devocional
pdg:
---
```

---

### 3️⃣ CITA (type: cita)

**Descripción:** Cita o reflexión sobre un libro, artículo, o pensamiento de otro autor.

**Campos obligatorios:**
- `type: cita`
- `mainpassage` — la cita/pasaje citado (puede ser de un libro)
- `otherpassages` — referencias bíblicas conexas (opcional)
- `series` — si es parte de un libro siendo estudiado (ej: "Lecturas de Tim Keller")
- `date` — cuándo capturaste/meditaste en la cita
- `tags` — incluir `Citas` + autor/fuente (ej: `Citas/Keller`)
- `related` — temas teológicos o bíblicos que conectan
- **No** necesita: `sequence`, `preacher`, `audience`, `pdg`

**Ejemplo:**
```yaml
---
type: cita
mainpassage: "Cita de Tim Keller sobre la Gracia"
otherpassages:
* "[[Rom 3]]"
* "[[Efe 2]]"
series: "[[Lecturas: Redención - Keller]]"
related:
  - "[[Gracia]]"
  - "[[Justificación]]"
  - "[[Evangelio]]"
date: 2025-08-22T14:30
tags:
  - Citas
  - Citas/Keller
  - Teología
pdg:
---
```

---

### 4️⃣ TOPICO (type: topico)

**Descripción:** Documento que desarrolla/analiza un tema bíblico o teológico específico.

**Campos obligatorios:**
- `type: topico`
- `mainpassage` — pasaje principal que define el tema
- `otherpassages` — pasajes que desarrollan el tema
- `related` — subtemas o temas conexos
- `date` — cuándo fue creado/actualizado
- `tags` — `Topicos` + categoría temática
- **Opcional**: `series`, `sequence`, `preacher`, `audience`, `pdg`

**Ejemplo:**
```yaml
---
type: topico
mainpassage: "[[Rom 5-8]]"
otherpassages:
* "[[Rom 1]]"
* "[[Gal 2]]"
* "[[1 Juan 1]]"
series:
related:
  - "[[Justificación]]"
  - "[[Santificación]]"
  - "[[Seguridad de salvación]]"
  - "[[Libre albedrío]]"
  - "[[Soberanía de Dios]]"
date: 2024-11-12T09:00
tags:
  - Topicos
  - Topicos/Soteriología
pdg:
---
```

---

## Índices de Referencia {#índices-de-referencia}

### 📖 indice_biblia.md
- **Ubicación:** Raíz del vault
- **Contenido:** Todos los libros y capítulos bíblicos en formato Obsidian-link
- **Formato de referencia:** `[[Libro Cap]]` ej: `[[2 Tim 3]]`, `[[Mat 16]]`, `[[Ap. 7]]`
- **Libros disponibles:** Revy (Rev), Ap., Acts, 1 Cor, 2 Tim, Jer, Mat, Rom, Heb, etc.

**Cómo usar:**
1. Abre `indice_biblia.md`
2. Busca el libro (ej: "2 Tim")
3. Encuentra el capítulo (ej: "2 Tim 3")
4. Copia el formato exacto: `[[2 Tim 3]]`

### 📚 Indice de temas biblicos.md
- **Ubicación:** Raíz del vault
- **Contenido:** Todos los temas teológicos/bíblicos del vault
- **Nota importante:** Incluye temas "master" marcados como principales
- **Formato:** Busca el tema exacto y copia con su capitalización exacta

**Cómo usar:**
1. Abre `Indice de temas biblicos.md`
2. Busca temas relevantes al contenido
3. Selecciona 4-8 temas que mejor describan el contenido
4. Prioriza temas principales/específicos sobre genéricos
5. Respeta la capitalización exacta

**Ejemplos de temas relevantes por tipo:**
- **Sermón sobre Gracia:** Gracia, El evangelio, Vida cristiana, Santificación, Soberanía de Dios
- **Meditación en Salmo:** Confianza en Dios, Protección de Dios, Paz, Adoración, Dependencia

---

## Notas sobre Evolución {#notas-sobre-evolución}

⚠️ **IMPORTANTE:** El sistema de frontmatter ha evolucionado a lo largo de los años.

### Cambios históricos conocidos:
- **2023:** Formato inicial inconsistente (sin YAML, metadatos ad-hoc)
- **2024:** Inicio de uso de YAML frontmatter
- **2025-2026:** Formato estandarizado actual (este documento)

### Qué esperar al revisar archivos viejos:
- Algunos archivos pueden tener metadatos en formato no-YAML (ej: "Pasaje bíblico:", "Fecha de predicación:")
- Campos faltantes o con nombres diferentes
- Fechas en diferentes formatos
- Referencias a libros no en indice_biblia.md

### Cómo manejar inconsistencias:
1. **Si el contenido es valioso:** Actualiza el frontmatter al formato actual
2. **Si hay dudas sobre temas:** Consulta el contenido del archivo para inferir temas relevantes
3. **Si no hay fecha:** Estima basándote en contexto (ej: serie de sermones con fechas cercanas)
4. **Si no hay audiencia:** Deja como `audience: [[Desconocida]]` o infiere del contexto
5. **Mantén el contenido intacto** — solo actualiza el frontmatter

---

## Checklist de Revisión {#checklist-de-revisión}

Cuando revises un archivo (antiguo o nuevo) y actualices/corrijas metadatos, verifica:

### Estructura
- [x] Frontmatter comienza con `---` en línea 1 [completion:: 2026-04-01]
- [x] Frontmatter termina con `---` antes del contenido [completion:: 2026-04-01]
- [x] Todos los campos están presentes (aunque algunos vacíos) [completion::2026-04-01]
- [x] Orden de campos es consistente [completion:: 2026-04-01]

### Contenido del Frontmatter
- [x] `type` es válido (sermon, meditacion, cita, topico) [completion:: 2026-04-01]
- [x] `mainpassage` tiene formato correcto: `[[Libro Cap]]` [completion:: 2026-04-01]
- [x] Pasajes están en indice_biblia.md (si son bíblicos) [completion:: 2026-04-01]
- [x] Temas en `related` están en Indice de temas biblicos.md [completion::2026-04-01]
- [x] `date` en formato ISO: `YYYY-MM-DDTHH:MM` [completion:: 2026-04-01]
- [x] `sequence` es número entero (si aplica) [completion:: 2026-04-01]
- [x] `preacher` es `[[Quique]]` o nombre correcto (para sermones) [completion:: 2026-04-01]
- [x] `audience` está documentada [completion:: 2026-04-01]
- [x] `tags` incluyen categoría principal (Sermones, Meditaciones, etc.) [completion:: 2026-04-01]

### Referencias Internas
- [x] Los links `[[...]]` corresponden a notas existentes (o que debería crear) [completion:: 2026-04-01]
- [x] No hay typos en nombres de temas/libros [completion:: 2026-04-01]
- [x] Capitalización es consistente [completion:: 2026-04-01]

### Completitud
- [x] El contenido concuerda con los metadatos [completion:: 2026-04-01]
  - ej: si dice `type: sermon`, tiene contenido de sermón (estructura, argumento, etc.)
- [x] `related` temas tienen lógica — reflejan el contenido real [completion:: 2026-04-01]
- [x] Si es serie, el `sequence` tiene sentido con otros elementos de la serie [completion::2026-04-01]

---

## Ejemplos Rápidos de Referencia

### Referencia rápida de formatos de libros:
```
Mat, Mark, Luke, Juan (not John)
1 Cor, 2 Cor (not Corintios)
Rom (not Romanos)
Gal (not Gálatas)
Efe (not Efesios)
Fil (not Filipenses)
Col (not Colosenses)
1 Thess, 2 Thess
1 Tim, 2 Tim, Tit (not Timoteo, Tito)
Philem
Heb (not Hebreos)
Jud (not Judas)
1 Juan, 2 Juan, 3 Juan
1 Pet, 2 Pet
Ap. (not Rev or Apocalipsis) — Nota el punto
Acts (not Hechos)
Sal (not Salmos)
Prov (not Proverbios)
Jer (not Jeremías)
Isa (not Isaías)
Lam (not Lamentaciones)
Dan (not Daniel)
Hos (not Oseas)
Joel, Amos, Obad, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi
```

---

## ⚠️ Detalles críticos del formato {#detalles-criticos}

### Cierre del frontmatter

**INCORRECTO:**
```yaml
pdg:---
```

**CORRECTO:**
```yaml
pdg:
---
```

**Regla:** Después de `pdg:` DEBE haber un salto de línea (enter) antes de `---`.

Sin el salto de línea, Obsidian y los parsers YAML pueden no reconocer correctamente el cierre del frontmatter.

---

## Banners de serie {#banners}

### Sistema actual (Feb 2026 en adelante)

Los banners ya **no se incluyen como propiedad del frontmatter**. En lugar del antiguo campo `banner:`, ahora se usa un CSS personalizado y el banner se coloca como la **primera línea del cuerpo**, justo después del cierre `---` del frontmatter:

```markdown
---
type: sermon
mainpassage: "[[Efesios 1.1-2]]"
...
pdg:
---
![[Nombre-del-banner|banner]]

# Título del sermón
```

### Sistema anterior (obsoleto)

```yaml
# ❌ Ya no usar — campo banner: en frontmatter
banner: Files/banners/Efesios-banner.jpg
```

### Reglas

- El banner va en la **primera línea del body**, antes del título y de cualquier otro contenido
- Usar el alias `|banner` para que el CSS lo reconozca como banner de página
- El nombre del archivo de imagen va sin ruta (solo el nombre del archivo, sin `Files/banners/`)
- **No incluir** el campo `banner:` en el frontmatter YAML

### Ejemplo por serie

| Serie | Línea de banner |
|-------|----------------|
| Efesios | `![[Efesios-banner\|banner]]` |
| Apocalipsis | `![[Apocalipsis-banner\|banner]]` |

---

## Manejo de Tópicos Bíblicos Faltantes {#topicos-faltantes}

### Problema común
A veces usarás un tópico bíblico en un frontmatter que **no existe** en el `Indice de temas biblicos.md`. Esto ocurre cuando:
- Usas temas muy específicos que no están documentados
- Creas frontmatters sin verificar el índice
- Necesitas temas nuevos que mejor organicen tu vault

### Solución: Crear nuevo tópico

Si identificas un tópico que falta, puedes **indicarle a Claude que:**

1. **Crear el archivo del tópico** con estructura completa
2. **Incluir frontmatter** tipo `TopicoBiblico`
3. **Agregar temas relacionados** (related)
4. **Actualizar el índice** en orden alfabético
5. **Corregir frontmatters** que usen ese tópico

### Ejemplo de instrucción:

```
"Identifiqué estos tópicos faltantes en Apocalipsis:
- Apostasía
- Testimonio
- Cielo

Por favor:
1. Crea archivos para cada uno con contenido apropiado
2. Agrégalos al Indice de temas biblicos.md en orden alfabético
3. Actualiza los frontmatters de Apocalipsis que usan estos tópicos"
```

### Estructura de un tópico bíblico {#estructura-topico}

```yaml
---
type: TopicoBiblico
title: [Nombre del tópico]
parent: "[[Tópico padre si existe]]"
related:
  - "[[Tópico relacionado 1]]"
  - "[[Tópico relacionado 2]]"
  - "[[Tópico relacionado 3]]"
tags:
  - TemasBiblicos
master: "[[Tema master relacionado]]"
---

# [Nombre del Tópico]

## Definición
[Descripción clara del concepto]

## Características bíblicas
- [Característica 1]
- [Característica 2]

## Pasajes clave
- [Pasaje relevante]
- [Pasaje relevante]
```

### Cambios de tópicos en frontmatters

Si necesitas **actualizar tópicos** en múltiples frontmatters (ej: cambiar "Juicio" por "Juicio de Dios"), puedes instruir:

```
"En todos los sermones de [Serie], cambia estos tópicos:
- Fidelidad → Fidelidad a Dios
- Juicio → Juicio de Dios
- Elimina: Plaga, Seducción, Visión"
```

---

## Contacto / Actualizaciones

Si necesitas actualizar este documento, considera:
- Agregar nuevo tipo de contenido
- Documentar cambios al sistema
- Corregir inconsistencias descubiertas
- Agregar ejemplos adicionales
- Actualizar el proceso de tópicos faltantes si cambia

**Última actualización:** Feb 17, 2026 (v2.1 - Agregado manejo de tópicos faltantes)