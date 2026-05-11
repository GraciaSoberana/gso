# INSTRUCCIONES: Revisión Diaria de Notas Devocionales

## Propósito
Este documento contiene las instrucciones para revisar y mejorar las notas devocionales del día, actualizando metadatos y corrigiendo ortografía.

---

## Contexto del Sistema

### Estructura de archivos
- **Carpeta principal**: `/mnt/Claude/`
- **Carpeta de trabajo diario**: `/mnt/Claude/today/`
- **Índice maestro**: `Indice de temas biblicos.md` (383+ tópicos bíblicos disponibles)
- **Template de frontmatter**: `ejemplo de frontmatter para TopicoBiblico.md`

### Contenido en carpeta "today"
1. **Daily Note** (formato: `YYYY-MM-DD.md`): Registro híbrido de devocional, seguimiento diario y actividades
2. **Notas devocionales**: Reflexiones sobre la lectura bíblica del día (generalmente 3-5 archivos)

---

## Tareas a Realizar

### 1. Actualizar Property "related"

#### Objetivo
Agregar tópicos bíblicos pertinentes del índice maestro a cada nota devocional.

#### Proceso
1. Leer el contenido completo de cada archivo en `/mnt/Claude/today/`
2. Identificar temas teológicos y bíblicos presentes en:
   - Las reflexiones personales del autor
   - Los pasajes bíblicos citados
   - Los conceptos doctrinales mencionados
3. Buscar los tópicos correspondientes en `Indice de temas biblicos.md`
4. Agregar los tópicos relevantes a la property `related:` en formato:
   ```yaml
   related:
     - "[[Nombre del Tópico]]"
     - "[[Otro Tópico]]"
   ```

#### Criterios para seleccionar tópicos
- **Temas principales** del pasaje bíblico (ej: Gracia, Justicia de Dios, Soberanía)
- **Conceptos doctrinales** mencionados (ej: Arrepentimiento, Santificación)
- **Atributos de Dios** revelados (ej: Paciencia de Dios, Omnipotencia)
- **Condiciones humanas** descritas (ej: Dureza de corazón, Pecado)
- **Respuestas espirituales** indicadas (ej: Oración, Adoración, Gratitud)

#### Cantidad recomendada
- **Daily Note**: 7-10 tópicos (cubre múltiples temas)
- **Notas devocionales individuales**: 4-7 tópicos (más específicas)

---

### 2. Corrección Ortográfica

#### REGLA CRÍTICA
**NUNCA editar texto bíblico** - Solo corregir las reflexiones personales del autor.

#### Qué corregir
✅ **Texto del autor** (reflexiones, oraciones, pensamientos personales):
- Acentuación (qué, cuándo, cómo vs que, cuando, como)
- Tildes faltantes (decisión, después, semáforo)
- Errores tipográficos (persoan → persona)
- Mayúsculas iniciales en preguntas/exclamaciones

❌ **NO tocar**:
- Versículos bíblicos (cualquier texto entre `> **número**` y el siguiente `>`)
- Referencias bíblicas
- Nombres propios bíblicos
- Citas textuales de las Escrituras

#### Errores comunes a vigilar
- "Que" → "Qué" (en exclamaciones/preguntas)
- "Cuando" → "Cuándo" (en preguntas)
- "Como" → "Cómo" (en preguntas)
- "ayudame" → "ayúdame"
- "compasion" → "compasión"
- "asi" → "así"
- Mayúsculas inconsistentes en pronombres divinos (opcional, seguir preferencia del autor)

---

## Flujo de Trabajo Recomendado

### Paso 1: Inventario
```bash
ls -lah /mnt/Claude/today/
```

### Paso 2: Lectura completa
Leer TODOS los archivos en la carpeta "today" para entender:
- El pasaje bíblico del día
- Los temas teológicos principales
- Las reflexiones del autor

### Paso 3: Consultar índice
Tener abierto el `Indice de temas biblicos.md` como referencia de tópicos disponibles.

### Paso 4: Editar uno por uno
Para cada archivo:
1. Actualizar `related:` con tópicos pertinentes
2. Corregir ortografía en reflexiones personales
3. Verificar que NO se tocó texto bíblico

### Paso 5: Reporte final
Resumir al usuario:
- Archivos procesados
- Tópicos agregados por archivo
- Correcciones ortográficas realizadas
- Cualquier observación relevante

---

## Ejemplo de Edición

### ANTES
```yaml
---
type: NotaDevocional
date: 2026-02-11
passage:
   - "[[Jer 5#3]]"
related:
---
```

```markdown
- Que terrible, pero esta es nuestra realidad humana...
```

### DESPUÉS
```yaml
---
type: NotaDevocional
date: 2026-02-11
passage:
   - "[[Jer 5#3]]"
related:
  - "[[Dureza de corazón]]"
  - "[[Arrepentimiento]]"
  - "[[Espíritu Santo]]"
  - "[[Depravación total]]"
  - "[[Conciencia de pecado]]"
---
```

```markdown
- Qué terrible, pero esta es nuestra realidad humana...
```

---

## Tópicos Frecuentes por Tema

### Cuando el pasaje habla de...
- **Juicio divino**: Justicia de Dios, Ira de Dios, Juicio final, Consecuencias del pecado
- **Dureza humana**: Dureza de corazón, Depravación total, Pecado, Arrepentimiento
- **Gracia y perdón**: Gracia, Perdón de pecados, Misericordia de Dios, Amor de Dios
- **Soberanía**: Soberanía de Dios, Providencia de Dios, Voluntad de Dios
- **Temor reverente**: Temor de Dios, Adoración, Santidad de Dios
- **Profecía falsa**: Predicación Expositiva, Autoridad de las Escrituras, Ministerio pastoral
- **Atributos creativos**: Omnipotencia, Omnipresencia, Creación, Providencia de Dios
- **Respuesta del creyente**: Oración, Santificación, Arrepentimiento, Fe, Obediencia

---

## Notas Adicionales

- **Los 13 Master Topics** (temas principales del sistema):
  1. Biblia
  2. Cristo
  3. Dios padre
  4. Escatología
  5. Espíritu Santo
  6. Familia cristiana
  7. Iglesia
  8. Pecado
  9. Salvación
  10. Santificación
  11. Teología bíblica
  12. Teología práctica
  13. Ética y cultura

- **Priorizar tópicos específicos** sobre generales (ej: "Dureza de corazón" mejor que solo "Pecado")
- **No duplicar** tópicos que ya estén en la lista
- **Mantener formato** exacto de wiki-links: `"[[Nombre del Tópico]]"`

---

## Comando Rápido para el Usuario

Simplemente carga este archivo y di:

> "Revisa las notas de today según las instrucciones"

O más breve:

> "Ejecuta la revisión diaria"

---

**Creado**: 2026-02-11
**Versión**: 1.0
**Uso**: Cargar al inicio de cada sesión de revisión diaria
