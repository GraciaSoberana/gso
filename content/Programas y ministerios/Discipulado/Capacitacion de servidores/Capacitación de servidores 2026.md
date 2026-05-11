---
publish: true
type: program
parent: "[[Discipulado y entrenamiento]]"
area: "[[Ministerial]]"
rama: "[[Discipulado y entrenamiento]]"
related:
  - "[[Masculinidad]]"
files: "[[capacitacion de servidores.af]]"
tags:
  - Calendario
  - entrenamiento
---


---

### La necesidad

1. El Señor no ne

- [[El ministerio cristiano (Spurgeon)]]
- [[El ministerio personal depende de una relacion personal]]

---
### Nuestras convicciones


---
### Qué buscamos

Que todos los servidores involucrados en la enseñanza crezcan en las siguientes áreas:

#### Cognitivas
1. Una comprensión clara del evangelio y su centralidad
2. Visión general de la Biblia
3. Teología bíblica
4. Teología sistemática
5. Identidad de Gracia Soberana
6. Ética cristiana

#### Relacionales


#### Bases discipulado


---

#### Calendario

- [[Evangelio, vida y ministerio]]
- [[Panorama bíblico - la ley]]
- [[Teología y doctrina 1]]
- [[Dinámicas del cambio biblico]]
---
#### Agenda

```base
filters:
  and:
    - master == link("Capacitación de servidores 2026")
    - type == "enseñanza"
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
      - series
      - date
    sort:
      - property: date
        direction: ASC
      - property: sequence
        direction: ASC
    columnSize:
      note.sequence: 46
      file.name: 309

```
