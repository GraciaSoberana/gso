---
publish: true
type: program
area: "[[Ministerial]]"
rama: "[[Discipulado y entrenamiento]]"
parent: "[[Escuela dominical]]"
responsable: "[[Ivan]]"
servidores:
  - "[[Hector]]"
  - "[[Quique Fonseca]]"
---

```dataview
TABLE seguimiento-2023-10-29 AS seguimiento
FROM "Personas/Personas" AND #Personas
where relation != [[ausentes]] AND sundaygroup = "teens"
SORT tag ASC 
```
