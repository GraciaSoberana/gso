---
publish: true
type: series
area: "[[Ministerial]]"
rama: "[[Discipulado y entrenamiento]]"
master: "[[Discipulados por rol familiar]]"
parent: "[[Talleres de matrimonios]]"
star: 2026-01-23
related:
  - "[[Centralidad del evangelio]]"
tags:
  - Ministerial/Intercesion
audience: "[[Gracia Soberana Orizaba]]"
---

```base
filters:
  and:
    - series == link("Matrimonios 26")
properties:
  note.sequence:
    displayName: "#"
  file.name:
    displayName: Tema
  note.date:
    displayName: Fecha
views:
  - type: table
    name: Table
    order:
      - sequence
      - file.name
      - date
    sort:
      - property: file.name
        direction: DESC

```

