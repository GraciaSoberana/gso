# Pergamino — Templates de referencia

## Frontmatter base

```yaml
---
theme: pergamino
width: 1000
height: 1500
---
```

---

## Template 1 · Solo versículo `tpl-perg-versiculo`

Para un versículo que se sostiene solo. Cita grande centrada + referencia + logo.
Variables: `versiculo`, `referencia`

```markdown
<!-- slide template="[[tpl-perg-versiculo]]" -->

::: versiculo
El SEÑOR es Rey eternamente y para siempre;
Las naciones han perecido de Su tierra.
:::

::: referencia
Salmo 10:16
:::
```

---

## Template 2 · Devocional diario `tpl-perg-devocional`

Día → cita → autor → separador → reflexión → logo.
Variables: `dia`, `cita`, `autor`, `reflexion`

```markdown
<!-- slide template="[[tpl-perg-devocional]]" -->

::: dia
Lunes
:::

::: cita
La verdadera espiritualidad se demuestra
en la vida diaria, no solo en la iglesia.
:::

::: autor
Martyn Lloyd-Jones
:::

::: reflexion
Tu fe se vive en cada acción de la semana.
:::
```

---

## Template 3 · Cita de autor `tpl-perg-cita`

Etiqueta → cita → autor → obra (opcional) → logo.
Variables: `dia`, `cita`, `autor`, `libro` (opcional)

```markdown
<!-- slide template="[[tpl-perg-cita]]" -->

::: dia
Cita
:::

::: cita
La gracia no es simplemente leniencia cuando
pecamos. La gracia es el poder de Dios para
no pecar.
:::

::: autor
John Piper
:::

::: libro
Gracia Futura
:::
```

---

## Template 4 · Reflexión propia `tpl-perg-reflexion`

Etiqueta → pensamiento grande → separador → reflexión → logo.
Variables: `dia`, `pensamiento`, `reflexion`

```markdown
<!-- slide template="[[tpl-perg-reflexion]]" -->

::: dia
Reflexión
:::

::: pensamiento
¿Cómo se ve tu fe en las
decisiones de esta semana?
:::

::: reflexion
La fe que no se practica en lo cotidiano
es solo una idea, no una convicción.
:::
```

---

## Nota sobre el logo

El logo GSO se posiciona automáticamente en la parte inferior
centrado en todos los templates. No necesitas incluirlo en tu nota.

El CSS del logo en los templates es:
```
filter: brightness(0); opacity: 0.38;
```
Esto convierte el logo (blanco) en un gris oscuro cálido sobre el fondo crema.
Para ajustar la intensidad, modifica el valor de `opacity` en el template correspondiente.
