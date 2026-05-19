# CLEANUP-REPORT — Lección 19

**Fecha:** 2026-05-18  
**Origen:** Exportación de Advanced Slides (Obsidian)  
**Destino:** `quartz/static/slides/19/` (Quartz v4, tema Abyssal)

---

## Resumen

| Métrica | Antes | Después | Δ |
|---------|-------|---------|---|
| Peso total | 28 MB | 26 MB | −2 MB |
| Número de archivos | 226 | 192 | −34 |

---

## Cambios realizados

### 1. Bloque de integración con Obsidian eliminado
**Archivo:** `index.html`  
**Líneas eliminadas:** ~19 líneas de JS (bloque `<script>` con `forgetPop`, `onPopState`, `window.onmessage` y el segundo `parent.postMessage`)  
**Razón:** Las llamadas `parent.postMessage(…, "app://obsidian.md")` son callbacks para comunicación con el iframe de Obsidian. Fuera de Obsidian son inoperantes pero innecesarias para hosting web.  
**Impacto funcional:** Ninguno. El modo `print-pdf` se conservó.

### 2. Background externo self-hosteado
**Archivos modificados:** `dist/theme/mygreek.css` (líneas 40 y 53), `css/gso-greek.css` (línea 102)  
**Cambio:** `http://graciasoberana.surge.sh/newbackground.png` → ruta relativa local  
- En `mygreek.css`: `../../css/newbackground.png`  
- En `gso-greek.css`: `newbackground.png`  

**Archivo añadido:** `css/newbackground.png` (24 KB, PNG 1920×1080)  
**Razón:** URL externa de `surge.sh` que se rompería si el hosting de surge caduca o cambia. El fondo es visual crítico del tema activo.

### 3. Temas de reveal.js no usados eliminados
**Tema activo conservado:** `dist/theme/mygreek.css`  
**Archivos eliminados (19 CSS):**
- `beige.css`, `black.css`, `blood.css`, `bruma.css`, `consult.css`
- `league.css`, `mattropolis.css`, `moon.css`, `mypurple.css`, `myquote.css`
- `mytheme.css`, `night.css`, `nocturno.css`, `pergamino.css`, `serif.css`
- `simple.css`, `sky.css`, `solarized.css`, `white.css`

**Carpeta eliminada:** `dist/theme/fonts/` (Source Sans Pro en `.woff`/`.ttf`/`.eot`, usada solo por temas eliminados)  
**Ahorro:** 2.3 MB → 16 KB (en `dist/theme/`)

---

## Decisiones no aplicadas (por elección del usuario)

- **Google Fonts externas:** Se conservaron las referencias a `fonts.googleapis.com` en `dist/theme/mygreek.css` (Montserrat, Noto Serif, Noto Sans Mono). Requieren conexión a internet para cargar las fuentes.
- **Notas del predicador:** Se conservaron los 31 bloques `<aside class="notes">`. Accesibles en modo presentador con la tecla `S`.
- **Contenido textual:** No se modificó ningún texto, griego bíblico, citas ni slides.
- **Imágenes:** No se recomprimieron ni convirtieron. Las 7 imágenes de paradigmas griegos están intactas.

---

## Rutas problemáticas — estado final

| Patrón | Estado |
|--------|--------|
| `file://` | No encontrado |
| `/home/` | No encontrado |
| `/Users/` | No encontrado |
| `/mnt/` | No encontrado |
| `app://obsidian.md` | Eliminado |
| `graciasoberana.surge.sh` | Eliminado → local |

---

## Historial git de esta copia

```
ade25cb  chore: snapshot inicial antes de limpieza
f8399bf  fix: eliminar bloque de integración con Obsidian (postMessage app://obsidian.md)
2e5da20  fix: self-hostear newbackground.png (era http://graciasoberana.surge.sh)
9e3e299  chore: borrar 19 temas de reveal.js no usados + carpeta fonts/
```
