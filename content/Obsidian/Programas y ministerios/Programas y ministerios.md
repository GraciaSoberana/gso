---
publish: true
---
### Series de predicación


### Discipulados y cursos

- [[Arraigados]]
- [[La travesía]]
- [[Puntos de Gracia]]
- [[Equipo de intercesión]]


| Horario  | Lunes               | Martes                                       | Miércoles                               | Jueves                                         | Viernes                          | Sábado  | Domingo                   |
|----------|---------------------|----------------------------------------------|-----------------------------------------|------------------------------------------------|----------------------------------|---------|---------------------------|
| Mañana   | —                   | La travesía mujeres                          |                                         |                                                |                                  |         | Culto                     |
| Tarde    | PDG Córdoba Norte   | La travesía hombres                          | Consejería                              | PDG Nogales                                    |                                  |         |                           |
| Noche    | —                   | PDG Norte<br>PDG Censos<br>PDG Mendoza       | Arraigados<br>La travesía mujeres       | La travesía hombres<br>PDG Córdoba Sur         | Reunión de equipo de intercesión | Act Esp | Evangelismo Hospital Civil |


### Actividades especiales

Todas las actividades que no forman parte de la semana cotidiana

```base
filters:
  and:
    - file.tags.containsAny("Evento")
properties:
  file.name:
    displayName: Tema
  note.sequence:
    displayName: "#"
  note.date:
    displayName: Fecha
  note.master:
    displayName: Ministerio
  note.parent:
    displayName: Ministerio
views:
  - type: table
    name: Todos
    order:
      - file.name
      - date
      - parent
    sort:
      - property: date
        direction: ASC
  - type: table
    name: Capacitación de servidores
    filters:
      and:
        - parent == link("Capacitación de servidores 26")
    order:
      - sequence
      - file.name
      - series
      - date
    sort:
      - property: date
        direction: ASC
  - type: table
    name: Reunión de intercesión
    filters:
      and:
        - parent == link("Reunión mensual de intercesión")
    order:
      - sequence
      - file.name
      - date
      - master
    sort:
      - property: date
        direction: ASC
  - type: table
    name: Reunión de matrimonios
    filters:
      and:
        - parent == link("Talleres de matrimonios")
    order:
      - sequence
      - file.name
      - date
    sort:
      - property: date
        direction: ASC
  - type: table
    name: Hombres
    filters:
      and:
        - parent == link("Hombres en verdad")
    order:
      - sequence
      - file.name
      - date
    sort:
      - property: date
        direction: ASC
  - type: table
    name: Mujeres
    filters:
      and:
        - parent == link("Mujeres de Gracia")
    order:
      - sequence
      - file.name
      - date
    sort:
      - property: date
        direction: ASC
```


---

```dataview
CALENDAR date
FROM #Evento/2026 
```