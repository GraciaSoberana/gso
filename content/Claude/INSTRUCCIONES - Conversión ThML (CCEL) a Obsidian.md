# Instrucciones: Conversión ThML (CCEL) a Notas Obsidian

**Versión:** 1.0 (Marzo 2026)
**Script:** `xml_to_obsidian.py` (raíz del vault)
**Propósito:** Convertir libros clásicos del formato ThML XML (CCEL) a notas Markdown para Obsidian

---

## ¿Qué es ThML?

ThML (Theological Markup Language) es el formato XML usado por la **Christian Classics Ethereal Library (CCEL)**. Cada libro es un archivo `.xml` con:

- `<ThML.head>` — metadatos del libro (título, autor, editorial, año)
- `<ThML.body>` — contenido dividido en `<div1>` (capítulos) y `<div2>` (subsecciones)

Los metadatos siguen el estándar Dublin Core (`DC.Title`, `DC.Creator`, `DC.Publisher`, etc.).

---

## Cómo usar el script

### Convertir un archivo individual

```bash
python3 xml_to_obsidian.py "Claude/xmls para convertir/grace.xml"
```

### Convertir todos los XMLs de una carpeta

```bash
python3 xml_to_obsidian.py "Claude/xmls para convertir"
```

### Opciones disponibles

| Opción | Descripción |
|--------|-------------|
| `--output <ruta>` | Carpeta de destino (por defecto: `Biblioteca/Libros`) |
| `--force` | Sobreescribir notas ya existentes |

### Ejemplos

```bash
# Convertir un solo libro a la carpeta por defecto
python3 xml_to_obsidian.py "Claude/xmls para convertir/sermons.xml"

# Re-convertir todos forzando sobreescritura
python3 xml_to_obsidian.py "Claude/xmls para convertir" --force

# Convertir a una carpeta personalizada
python3 xml_to_obsidian.py "Claude/xmls para convertir/near.xml" --output "Biblioteca/Kuyper"
```

---

## Lógica de conversión

### Detección corta vs. larga

El script cuenta los capítulos reales del libro (omitiendo portadas e índices):

- **≤ 5 capítulos** → Un solo archivo `.md` con todo el contenido
- **> 5 capítulos** → Carpeta con un archivo índice + un `.md` por capítulo

### Estructura de capítulos

El script maneja dos estructuras comunes en ThML:

1. **div1 como capítulos** — cada `<div1>` es un capítulo (ej: *Select Sermons* de Edwards)
2. **div2 como capítulos** — el libro tiene pocos `<div1>` pero muchos `<div2>` dentro (ej: *Calvinism* de Kuyper)

El script detecta cuál aplica automáticamente. Se omiten siempre: "Title Page", "Indexes", "Table of Contents".

### Autor

El script extrae el autor del XML con esta prioridad:

1. `DC.Creator` sin scheme y con espacio → nombre completo legible
2. `DC.Creator scheme="short-form"` con espacio → nombre completo
3. `DC.Creator scheme="file-as"` → se parsea "Apellido, Nombre (años)" → "Nombre Apellido"

Luego el nombre se normaliza con la tabla `AUTHOR_NORMALIZE` del script (ver sección de normalización).

**Si el autor no existe en el Índice de Autores**, se crea automáticamente un archivo stub en `Biblioteca/01 Fuentes/Autores/` con:

```yaml
---
type: author
tags:
  - Biblioteca/Autores
---
```

### Temas relacionados

Se buscan automáticamente en `Claude/Indice de temas biblicos.md` usando coincidencia de palabras clave entre el título del libro, los títulos de capítulos y los temas disponibles. Se asignan hasta 4 temas por libro y hasta 3 por capítulo.

---

## Frontmatter generado

### Archivo índice / libro corto (`type: book`)

```yaml
---
type: book
title: "The Method of Grace in the Gospel Redemption"
author: "[[John Flavel]]"
publisher: "[[Christian Classics Ethereal Library]]"
year: 2000
tags:
  - resources/CCEL
related:
  - "[[Expiación particular]]"
  - "[[Gracia]]"
---
```

### Capítulo individual (`type: chapter`)

```yaml
---
type: chapter
title: "Sinners in the Hands of an Angry God"
author: "[[Jonathan Edwards]]"
parent: "[[Select Sermons]]"
publisher: "[[Christian Classics Ethereal Library]]"
year: 2000
tags:
  - resources/CCEL
related:
  - "[[Juicio final]]"
  - "[[Ira de Dios]]"
---
```

---

## Libros convertidos (estado actual)

| Archivo XML | Título | Autor | Capítulos | Formato |
|-------------|--------|-------|-----------|---------|
| `ascentofchrist.xml` | The Ascent of the Son — The Descent of the Spirit | Abraham Kuyper | 28 | Carpeta |
| `deut.xml` | Expositions of Holy Scripture: Deuteronomy… | Alexander Maclaren | 8 | Carpeta |
| `ezek_matt1.xml` | Expositions of Holy Scripture: Ezekiel… | Alexander Maclaren | 67 | Carpeta |
| `fountain.xml` | The Fountain of Life Opened Up | John Flavel | 44 | Carpeta |
| `gen_num.xml` | Expositions of Holy Scripture: Genesis… | Alexander Maclaren | 4 | Archivo único |
| `grace.xml` | The Method of Grace in the Gospel Redemption | John Flavel | 37 | Carpeta |
| `greater.xml` | You Can Do Greater Things Than Christ | Abraham Kuyper | 11 | Carpeta |
| `holy_spirit.xml` | The Work of the Holy Spirit | Abraham Kuyper | 25 | Carpeta |
| `islam.xml` | The Mystery of Islam | Abraham Kuyper | 14 | Carpeta |
| `lecture.xml` | Calvinism: Six Stone-lectures | Abraham Kuyper | 6 | Carpeta |
| `lovely.xml` | Christ Altogether Lovely | John Flavel | 6 | Carpeta |
| `near.xml` | To Be Near Unto God | Abraham Kuyper | 110 | Carpeta |
| `pneum.xml` | Pneumatologia: A Treatise of the Soul of Man | John Flavel | 10 | Carpeta |
| `sermons.xml` | Select Sermons | Jonathan Edwards | 20 | Carpeta |
| `works1.xml` | The Works of Jonathan Edwards, Volume One | Jonathan Edwards | 99 | Carpeta |
| `works2.xml` | The Works of Jonathan Edwards, Volume Two | Jonathan Edwards | 116 | Carpeta |

**Total: 599 notas generadas** (16 índices + 583 capítulos)

---

## Autores creados automáticamente

Los siguientes autores fueron creados en `Biblioteca/01 Fuentes/Autores/` durante la primera conversión:

- Abraham Kuyper
- Alexander Maclaren
- Jonathan Edwards
- John Flavel *(ya existía en el índice)*

---

## Normalización de autores

La tabla `AUTHOR_NORMALIZE` en el script mapea nombres del XML al nombre canónico del vault:

```python
AUTHOR_NORMALIZE = {
    "Juan Bunyan":            "John Bunyan",
    "John Charles Ryle":      "J. C. Ryle",
    "Joel Beeke":             "Joel R. Beeke",
    "Benjamin Keach":         "Benjamín Keach",
    "Robert Murray McCheyne": "Robert Murray M'Cheyne",
    "Vario":                  "Varios",
    "varios":                 "Varios",
}
```

Si agregas nuevos XMLs con autores que tienen un nombre diferente en el vault, agrega la entrada correspondiente antes de correr el script.

---

## Agregar nuevos XMLs

1. Coloca el archivo `.xml` en `Claude/xmls para convertir/`
2. Verifica si el autor ya está en `Claude/Indice de Autores.md`
   - Si tiene un nombre diferente en el XML, agrégalo a `AUTHOR_NORMALIZE` en el script
3. Corre el script:
   ```bash
   python3 xml_to_obsidian.py "Claude/xmls para convertir/nuevo_libro.xml"
   ```
4. Verifica la nota generada en `Biblioteca/01 Fuentes/Libros/`

---

## Notas técnicas

- Los archivos ThML que tienen el autor en `scheme="ccel"` (un identificador como `flavel`) no son problemáticos: el script ignora estos IDs y extrae el nombre legible de `scheme="short-form"` o del valor sin scheme.
- Las etiquetas `<scripRef>` (referencias bíblicas inline) se conservan como texto plano.
- Las etiquetas `<scripCom>` (pasaje base del sermón) se renderizan como *texto en itálica* al inicio del capítulo.
- El texto en `<b>` se convierte a `**negrita**` y en `<i>` a `_itálica_`.
- Los títulos de capítulos muy largos se truncan a 80 caracteres (a la palabra completa) para evitar errores de nombre de archivo.

---

## Contacto / Actualizaciones

Si necesitas actualizar este documento:
- Agregar nuevos libros convertidos a la tabla
- Documentar nuevos autores normalizados
- Registrar cambios en la lógica del script

**Última actualización:** Marzo 2026 (v1.0 — Conversión inicial de 16 XMLs CCEL)
