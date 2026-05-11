# Guía: Corregir metadatos de una serie completa

**Propósito:** Paso a paso para revisar, corregir y normalizar los metadatos de una serie de sermones.


---

## Fase 1: Análisis Inicial

### 1.1 Explorar la carpeta
```bash
ls "/ruta/a/la/carpeta/"
```
Obtén una lista completa de los archivos de la serie.

### 1.2 Revisar metadatos actuales
Lee 3-4 archivos para entender:
- Formato actual del frontmatter
- Qué campos existen
- Qué está faltando o es inconsistente
- Qué pasajes usan

### 1.3 Identificar problemas
Busca:
- ❌ Campos con nombres incorrectos (ej: `passage:` en lugar de `mainpassage:`)
- ❌ Formatos inconsistentes (ej: `[[Libro]]` vs `Libro X:Y`)
- ❌ Tópicos que **no existen** en el índice
- ❌ Fechas en formato incorrecto
- ❌ Campos faltantes (ej: `pdg:`, `otherpassages:`)

---

## Fase 2: Identificar Tópicos Faltantes

### 2.1 Extraer todos los tópicos usados
Recolecta todos los tópicos del campo `related:` de todos los archivos.

### 2.2 Verificar contra el índice
```python
# Comparar tópicos usados vs tópicos válidos
tópicos_usados = {...}
tópicos_válidos = {...}
faltantes = tópicos_usados - tópicos_válidos
```

### 2.3 Documentar faltantes
Crea una lista como esta:

| Tópico faltante | Equivalente en índice | Acción |
|---|---|---|
| Apostasía | ❌ NO EXISTE | Crear nuevo |
| Juicio | `[[Juicio de Dios]]` | Cambiar por |
| Plaga | ❌ NO EXISTE | Eliminar |

---

## Fase 3: Crear Tópicos Nuevos

### 3.1 Crear archivos
Para cada tópico faltante que **valga la pena crear**, genera un archivo:

**Estructura mínima:**
```yaml
---
type: TopicoBiblico
title: [Nombre]
parent: "[[Tópico padre si existe]]"
related:
  - "[[Tópico relacionado 1]]"
  - "[[Tópico relacionado 2]]"
tags:
  - TemasBiblicos
master: "[[Master tema]]"
---

# [Nombre del Tópico]

## Definición
[Explicación]

## Pasajes clave
- [Pasaje 1]
- [Pasaje 2]
```

### 3.2 Agregar al índice
Inserta cada nuevo tópico en orden alfabético en `Indice de temas biblicos.md`.

---

## Fase 4: Corregir Frontmatters de la Serie

### 4.1 Crear mapeo de correcciones

Crea una tabla con:
- Archivo
- Mainpassage correcto (en formato `[[Libro Cap]]`)
- Otherpassages
- Tópicos relacionados correctos

### 4.2 Cambios sistemáticos

**Cambios de nombres:**
- `passage:` → `mainpassage:`
- Tópicos genéricos → Específicos

**Cambios de valores:**
- `Libro X:Y` → `[[Libro X]]`
- `Juicio` → `Juicio de Dios`

**Eliminaciones:**
- Tópicos que no existen y no valen crear → eliminar

### 4.3 Normalización de formatos

Asegurate que todos los frontmatters tengan:
```yaml
---
type: sermon
mainpassage: "[[Libro Cap]]"
otherpassages:
* "[[Libro Cap]]"
series: "[[Nombre de la serie]]"
related:
  - "[[Tópico válido]]"
sequence: #
preacher: "[[Quique]]"
date: YYYY-MM-DDTHH:MM
tags:
  - Sermones
audience: "[[Audiencia]]"
pdg:
---
```

⚠️ **CRÍTICO:** Después de `pdg:` debe haber un **salto de línea** antes de `---`
- ❌ Incorrecto: `pdg:---`
- ✅ Correcto: `pdg:` + ENTER + `---`

---

## Ejemplo: Proceso con Apocalipsis

### Caso: Identifiqué 17 tópicos faltantes

**Decisión:**
- ✅ Crear 5: Apostasía, Boda del Cordero, Cielo, Fidelidad a Dios, Testimonio
- 🔄 Cambiar 8: Por equivalentes que sí existen
- ❌ Eliminar 4: Plaga, Seducción, Visión, etc.

**Comandos a Claude:**

1. **Crear nuevos tópicos:**
   ```
   "Crea archivos para estos 5 tópicos bíblicos:
   - Apostasía
   - Boda del Cordero
   - Cielo
   - Fidelidad a Dios
   - Testimonio

   Incluye:
   - Frontmatter tipo TopicoBiblico
   - Temas relacionados apropiados
   - Contenido breve con definición y pasajes clave"
   ```

2. **Actualizar índice:**
   ```
   "Agrega estos 5 nuevos tópicos al Indice de temas biblicos.md
   en orden alfabético"
   ```

3. **Corregir frontmatters:**
   ```
   "En todos los 22 sermones de Apocalipsis, realiza estos cambios:

   CAMBIOS DE NOMBRES:
   - Fidelidad → Fidelidad a Dios
   - Juicio → Juicio de Dios
   - Interpretación bíblica → Exégesis

   CAMBIOS ESPECIALES:
   - Llamamiento al arrepentimiento → [[Llamamiento eficaz]] + [[Arrepentimiento]]
   - Maranata → [[Venida de Cristo]]
   - Reinado de Cristo → [[Reino de Dios]]

   ELIMINAR:
   - Plaga
   - Seducción
   - Visión
   - Revelación (cambiar por Revelación especial)"
   ```

---

## Checklist Final

- [x] Todos los `mainpassage:` están en formato correcto [completion:: 2026-04-01]
- [x] Todos los `related:` existen en el índice [completion:: 2026-04-01]
- [x] Todos los archivos tienen `pdg:` (aunque vacío) [completion:: 2026-04-01]
- [x] Todos tienen `tags: - Sermones` [completion:: 2026-04-01]
- [x] Todas las fechas están en formato `YYYY-MM-DDTHH:MM` [completion:: 2026-04-01]
- [x] Orden de campos es consistente [completion:: 2026-04-01]
- [x] Sin tópicos duplicados o mal escritos [completion:: 2026-04-01]
- [x] El índice contiene todos los nuevos tópicos [completion:: 2026-04-01]

---

## Próximas veces

Cuando tengas una **nueva serie**, simplemente:

1. Di: "Revisa y corrige los metadatos de la serie **[Nombre]**"
2. Especifica si hay tópicos faltantes que quieres crear
3. Indica cambios específicos que quieres hacer
4. Claude seguirá este proceso automáticamente

**Ejemplo:**
```
"Revisa la serie 'Romanos' y:
1. Identifica tópicos que faltan
2. Propón cuáles crear y cuáles cambiar por equivalentes
3. Crea los nuevos tópicos
4. Actualiza el índice
5. Corrige todos los frontmatters"
```

---

**Documento creado:** Feb 17, 2026
**Basado en:** Proceso de corrección de serie Apocalipsis (22 sermones)