---
publish: true
type: series
area:
start: 2025-06-08
end:
related:
  - "[[Leviticus]]"
  - "[[Santidad de Dios]]"
  - "[[Santificación]]"
  - "[[Pureza e impureza ritual]]"
tags:
  - Sermones
files:
  - "[[levitico.afdesign]]"
---

![[levitico-banner.jpg|banner]]

[[Series de sermones]] basada en el libro de  [[Leviticus]], Predicada en Gracia Soberana Orizaba en Junio - 2025

#### [[Sermones en Levítico]]
```base
query:
  from: "#Sermones"
  where:
    type: sermon
    series: Llamados a vivir ante el Dios Santo (Levítico)
  sort:
    by: sequence
    order: asc
  view: table
  columns:
filters:
  and:
    - file.hasLink("Sermones/Levitico/Llamados a vivir ante el Dios Santo (Levítico)")
    - type == "sermon"
properties:
  note.sequence:
    displayName: "#"
  file.name:
    displayName: Sermón
  note.passage:
    displayName: Texto
  note.date:
    displayName: Fecha
views:
  - type: table
    name: Table
    order:
      - sequence
      - file.name
      - passage
      - date
      - pdg
    sort:
      - property: sequence
        direction: ASC
      - property: passage
        direction: ASC
    columnSize:
      file.name: 386

```

