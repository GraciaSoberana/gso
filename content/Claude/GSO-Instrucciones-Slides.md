# Instrucciones: Bosquejo → Slide GSO

## Contexto
- Iglesia: Gracia Soberana Orizaba (GSO)
- Plugin: Obsidian Advanced Slides 1.20.0
- Theme: `css/gso-theme.css`
- Resolución: 1920×1080 (16:9)
- Proyección: WorshipTools Presenter (vía PPTX convertido con `convertir.bat`)
- Tipografía grande por pantallas pequeñas → textos cortos por slide

---

## Estructura fija de toda presentación

```
1. Imagen fullscreen de la serie
2. Portada del sermón
3. Puntos principales (mapa del sermón)
4. Por cada punto:
   a. Slide de punto principal
   b. Textos bíblicos del punto (COMPLETOS pero con tamaño grande, si es necesario el versículo se parte en dos o tres partes)
   c. Citas o bullets intercalados según orden del sermón
```

---

## Frontmatter obligatorio

```yaml
---
type: slide
parent: "[[]]"
theme: css/gso-theme.css
width: 1920
height: 1080
transition: fade
margin: 0
minScale: 0.2
maxScale: 2
---
```

---

## Reglas de fragmentación de texto bíblico

- **Máximo ~15 palabras por slide**
- Frases largas se cortan en su punto natural (coma, conjunción, cambio de sujeto)
- Las continuaciones llevan `…` al inicio y/o final para indicar que el texto sigue
- El número de versículo se repite en cada fragmento del mismo versículo
- Corregir referencias incompletas (ej. `Daniel 6:` sin número)

---

## Templates disponibles y su sintaxis

### Imagen fullscreen
```markdown
<!-- slide template="[[tpl-gso-fullscreen]]" bg="black" -->

![[nombre-imagen.jpg|1920]]
```

### Portada
```markdown
<!-- slide template="[[tpl-gso-portada]]" -->

::: serie
Nombre de la serie · Libro
:::

::: titulo
Título del Sermón
:::

::: referencia
Un sermón en Libro capítulo
:::

::: predicador
Nombre Predicador · Fecha
:::
```

### Punto principal
```markdown
<!-- slide template="[[tpl-gso-punto]]" -->

::: numero
01
:::

::: titulo
Título del punto
:::
```
> Sin `::: subtitulo :::` a menos que el bosquejo lo indique explícitamente.

### Texto bíblico (fragmentado)
```markdown
<!-- slide template="[[tpl-gso-versiculo]]" -->

::: versiculo
Texto del fragmento (~15 palabras máx.)
:::

::: referencia
Libro capítulo:versículo
:::
```

### Bullets
```markdown
<!-- slide template="[[tpl-gso-bullets]]" -->

::: titulo
Título de la sección
:::

- Punto uno con **énfasis** si aplica
- Punto dos
- Punto tres
```

### Cita
```markdown
<!-- slide template="[[tpl-gso-cita]]" -->

::: cita
Texto de la cita.
:::

::: autor
— Nombre del Autor
:::
```

### Slide final
```markdown
<!-- slide template="[[tpl-gso-portada]]" -->

::: titulo
Soli Deo Gloria
:::

::: referencia
Gracia Soberana Orizaba
:::
```

---

## Datos que necesito del bosquejo

| Dato | Dónde lo busco |
|---|---|
| Nombre de la serie | Frontmatter o título del archivo |
| Título del sermón | H1 del bosquejo |
| Pasaje principal | Referencia bíblica del título |
| Nombre del predicador | Bosquejo o indicación explícita |
| Fecha | Indicación explícita |
| Imagen de la serie | Nombre del archivo .jpg/.png |
| Puntos principales | H2 del bosquejo |
| Textos bíblicos por punto | Citas en el cuerpo del bosquejo |
| Citas de autores | Callouts `[!quote]` o texto entre comillas |
| Bullets | Listas del bosquejo |

---

## Lo que NO hago automáticamente

- No invento fragmentaciones si el texto no está en el bosquejo
- No asumo el orden de slides dentro de un punto si no está claro
- No incluyo texto del manuscrito, solo lo que va en pantalla
- Si hay textos largos, pregunto cómo fragmentar antes de generar
