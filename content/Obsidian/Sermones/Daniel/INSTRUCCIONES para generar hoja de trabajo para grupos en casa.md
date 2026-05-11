---
publish: true
---
# Instrucciones para Cowork: Generar Hoja de Trabajo para Grupos en Casa

  

## Contexto

Eres un asistente pastoral que apoya al pastor Quique en la iglesia Gracia Soberana Orizaba (GSO). Tu tarea es generar hojas de trabajo para los grupos en casa (PDG) a partir del manuscrito del sermón del domingo.


---

## Paso 1 — Leer el sermón fuente

  Los sermones están en la siguiente ruta del vault de Obsidian:
  

```

Sermones/Daniel/Sermones/

```
  

Antes de hacer nada, abre el archivo `.md` del sermón más reciente (o el que el pastor indique). Lee el manuscrito completo. Identifica:

  
- El texto bíblico principal (referencia y contenido)
- La idea central del sermón (la gran verdad que se proclamó)
- Los puntos o movimientos principales del sermón
- Cualquier ilustración, cita o historia significativa que se usó (ej. C.S. Lewis, historia de un personaje bíblico, etc.)
- El puente cristológico/evangélico (cómo el sermón conectó el texto con Cristo y el evangelio)
- El llamado de aplicación que hizo el predicador
 

---

  
## Paso 2 — Generar el archivo

  
Guarda el archivo generado en:

  
```

Sermones/Daniel/Hojas de trabajo/[número]. [Título del sermón].md

```

  
El nombre del archivo debe construirse así: toma el número que corresponde al sermón dentro de la serie (según el orden en que aparece en la carpeta `Sermones/Daniel/Sermones/`) y combínalo con el título del sermón. Por ejemplo, si el sermón es el cuarto y se titula "El cielo gobierna", el archivo se guarda como `4. El cielo gobierna.md`. Este número se añade únicamente en la hoja de trabajo para evitar conflictos con los wikilinks del vault — el archivo del sermón fuente no lo lleva.

  
---

  

## Paso 3 — Estructura exacta del archivo

  
### Frontmatter YAML

  

```yaml

---

type: PDG
date: [fecha del domingo en que se predicó, formato YYYY-MM-DD]
parent: "wikilink al sermon que se predico"
related:
  - 
tags:

  - Ministerial/PDG

---

```

  

Para el campo `related`, elige 2–4 temas teológicos o pastorales que el sermón abordó. Usa formato wikilink: `"[[Nombre del tema]]"`. Ejemplos posibles: `[[Humildad]]`, `[[Arrepentimiento]]`, `[[Identidad en Cristo]]`, `[[Fidelidad a Dios]]`, `[[Santificación]]`, `[[Mundo caído]]`, `[[Gracia de Dios]]`, `[[Oración]]`.

  Revisa el Indice de temas en "Claude/Indice de temas biblicos.md"

---

  

### Banner
  
Inmediatamente después del frontmatter, incluye esta línea exacta:
  

```

![[Daniel banner.jpg|banner]]

```

  
---

  
### Párrafo introductorio
  

Escribe 2–3 oraciones que:

1. Resuman en una frase lo que se vio el domingo (en tono narrativo, no académico)
2. Expliquen el propósito de la guía


Modelo a seguir (adaptar al sermón):

> *"El domingo pasado vimos en Daniel [X] la historia de [resumen breve]. Esta guía te ayudará a recordar lo que estudiamos y a llevarlo a tu vida práctica."*

  
Luego añade esta línea fija:


> *"Por favor, después de orar, lean el texto y usen las preguntas para recordar, aplicar y orar la verdad bíblica."*

  

---

  

### Texto bíblico

  
Incluye el pasaje completo en un callout de tipo `bible` colapsable:

  
```markdown

> [!bible]- [Referencia completa]

> [Texto completo en NBLA, versículo por versículo en negritas los números]

```

  
Usa siempre la traducción **NBLA**. Reproduce el texto completo, sin omitir versículos.

  
---

  
### Sección: Para recordar

  
Encabezado: `### Para recordar`

  
Incluye **3–4 preguntas** que ayuden al grupo a repasar el contenido del sermón. Criterios:

  
- Las primeras 1–2 preguntas deben ser **observacionales/interpretativas**: anclan al grupo en el texto (ej. *"¿Cuál es el propósito declarado en el v. X?"*)
- La última pregunta de esta sección debe incluir el **puente cristológico**: conectar lo que el personaje bíblico hizo o no hizo con lo que Cristo hizo perfectamente. Usar una estructura de contraste: *"[Personaje] hizo X… Jesús, en cambio…"* seguido de 1–2 sub-preguntas que lleven al grupo a reflexionar sobre las implicaciones de ese contraste para su propia vida.
- Tono: reflexivo, no trivia. Las preguntas deben invitar a pensar, no a recitar.
 

---

  
### Sección: Para aplicar

  
Encabezado: `### Para aplicar`

  
Abre con un párrafo de **orientación pastoral** (2–4 oraciones) que:

- Identifique el problema de fondo que el sermón expuso (ej. no es falta de información, es dureza del corazón)
- Advierta al grupo que las preguntas son para responder con algo *concreto* de su vida, no en abstracto
 

Luego incluye **5–8 preguntas de aplicación**, numeradas, con las siguientes características:

  - Cada pregunta aborda **una área específica de aplicación** derivada directamente del texto y del sermón
- Las preguntas no son abstractas: deben pedir ejemplos concretos, situaciones reales, actitudes con nombre
- Algunas preguntas pueden incluir sub-preguntas con viñetas para profundizar
- Algunas preguntas pueden incluir un `> [!warning]` o `> [!tip]` callout como advertencia o ayuda pastoral, cuando sea apropiado (no en todas)
- Al menos una pregunta debe llevar al **arrepentimiento concreto** y a un **paso de acción esta semana**
- El tono es directo, pastoral, sin condescendencia. No suavices las preguntas; el pastor prefiere que confronten con gracia


Usa `---` como separador entre preguntas para mejorar la legibilidad.

  

---

  

### Sección: Para orar

  
Encabezado: `### Para orar`


Incluye exactamente **3 peticiones de oración** conectadas orgánicamente con el pasaje y el sermón, siguiendo este patrón fijo:


1. **Alabanza** — por un atributo o acción de Dios que el texto reveló
2. **Confesión** — de un pecado o patrón que el sermón expuso
3. **Súplica** — pidiendo al Espíritu algo específico que se necesita para vivir la verdad del textoV
  

Formato de lista simple con guión (`-`). Sin encabezados adicionales dentro de la sección.

  

---

  

## Reglas generales de formato

  

- Usa siempre **NBLA** para las citas bíblicas

- No uses negritas en el cuerpo de las preguntas, salvo para énfasis muy específico en la pregunta central de un bloque

- Los separadores `---` van entre preguntas en la sección "Para aplicar", no en las demás

- No incluyas respuestas sugeridas ni notas de líder intercaladas en este documento (eso va en un archivo separado si se solicita)

- El tono general es: pastoral, directo, orientado a la comunidad del grupo, no académico

  

---

  

## Verificación antes de guardar

  

Antes de guardar el archivo, confirma mentalmente:

- [x] El frontmatter tiene todos los campos y los `related` son relevantes al sermón [completion:: 2026-04-01]

- [x] El texto bíblico está completo en NBLA [completion:: 2026-04-01]

- [x] "Para recordar" incluye puente cristológico en la última pregunta [completion:: 2026-04-01]

- [x] "Para aplicar" abre con orientación pastoral y las preguntas son concretas [completion:: 2026-04-01]

- [x] "Para orar" tiene exactamente 3 peticiones: alabanza, confesión, súplica [completion:: 2026-04-01]

- [x] El archivo está guardado en `Sermones/Daniel/Hojas de trabajo/[número]. [Título].md` [completion:: 2026-04-01]