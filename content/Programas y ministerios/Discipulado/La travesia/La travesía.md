---
publish: true
type: program
parent: "[[Discipulado y entrenamiento]]"
area:
  - "[[Ministerial]]"
---
![[journey.jpg|banner]]

### Los contenidos

- [[La travesía (azul)]]
- [[La travesía (verde)]]
- [[La travesía (Rojo)]]

### Grupos 2026

```base
filters:
  and:
    - parent == link("La travesía")
    - type == "grupo"
views:
  - type: table
    name: Table

```

### Mi agenda

```base
filters:
  and:
    - parent == link("La travesía")
    - type == "discipulado"
views:
  - type: table
    name: Table
    order:
      - file.name
      - grupo
      - contenido
      - date
    sort:
      - property: grupo
        direction: ASC
      - property: date
        direction: ASC

```

