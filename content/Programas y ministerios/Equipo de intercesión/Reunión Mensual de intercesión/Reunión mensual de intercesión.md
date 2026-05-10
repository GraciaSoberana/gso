---
publish: true
type: programa
area: "[[Ministerial]]"
rama: "[[Oración]]"
responsable: "[[Quique]]"
auxiliar:
related:
  - "[[Filosofía ministerial de Gracia Soberana Orizaba]]"
  - "[[07 Convicciones para la dirección de la Iglesia]]"
  - "[[Impulsados por Gracia, Guiados por el Espíritu]]"
  - "[[Programas de oración]]"
  - "[[Gracia Soberana Orizaba]]"
files:
  - "[[Reunión mensual de intercesión.afdesign]]"
tags:
  - Ministerial/Intercesion
dg-publish: true
---

![[pray.jpg|banner]]

### Nuestra convicción

![[Impulsados por Gracia, Guiados por el Espíritu#^664e3e]]


### Nuestra meta:

![[Que Cada miembro de la iglesia conozca, ame y viva bajo el control del Espíritu  de tal manera que nuestras vidas, nuestra iglesia y nuestra comunidad sean transformadas por Su presencia#^PropositoOracion]]


### Nuestro programa

>  »Además les digo, que si dos de ustedes se ponen de acuerdo sobre cualquier cosa que pidan _aquí_ en la tierra, les será hecho por Mi Padre que está en los cielos. Porque donde están dos o tres reunidos en Mi nombre, allí estoy Yo en medio de ellos».<br ><span class="author">Mateo 18:19-20</span>


El Señor nos enseñó con claridad que cuando su pueblo se reúne para orar conforme a su voluntad el nos escucha. Por lo tanto, el objetivo de la *reunión mensual de intercesión* consiste en reunir a la iglesia local para orar.  Nos reuniremos el primer viernes de cada mes.



### Primer semestre: <br >[[Orando por una renovación en nuestro amor por Cristo]]

```base
filters:
  and:
    - series == link("Orando por una renovación en nuestro amor por Cristo")
properties:
  file.name:
    displayName: Tema
  note.sequence:
    displayName: "#"
  note.date:
    displayName: Fecha
views:
  - type: table
    name: Table
    order:
      - sequence
      - file.name
      - date
      - master
    sort:
      - property: sequence
        direction: ASC


```



### Segundo semestre 2026: <br >[[Orando por el fruto del evangelio]]

```base
filters:
  and:
    - series == link("Orando por el fruto del evangelio")
properties:
  file.name:
    displayName: Tema
  note.sequence:
    displayName: "#"
  note.date:
    displayName: Fecha
views:
  - type: table
    name: Table
    order:
      - sequence
      - file.name
      - date
      - master
    sort:
      - property: sequence
        direction: ASC
      - property: file.name
        direction: ASC
    columnSize:
      file.name: 380
    viewMode: calendar
    taskContent: file.basename
    taskStatus: note.status
    taskPriority: note.priority
    taskProject: note.project
    taskTags: note.tags
    taskDueDate: note.dueDate
    taskStartDate: note.startDate
    taskCompletedDate: note.completionDate
    taskContext: note.context

```


![[Pasted image 20260117100712.png]]

---
>[!links] Archivos:
>[Plantilla de anuncio](https://docs.google.com/presentation/d/1XWbB96yTZ3A4cZIqe6anG6bc1ApkQPKfc_yB1doil8Y/edit?usp=sharing)

