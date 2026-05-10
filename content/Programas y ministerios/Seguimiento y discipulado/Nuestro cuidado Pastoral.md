---
publish: true
type: programa
area: "[[Ministerial]]"
rama: "[[Pastoral]]"
responsable: "[[Quique]]"
auxiliar:
related:
  - "[[Filosofía ministerial de Gracia Soberana Orizaba]]"
  - "[[Gracia Soberana Orizaba]]"
  - "[[Familias de Gracia Soberana Orizaba]]"
tags:
  - Ministerial
---
![[pastoral.jpg|banner]]

>   Pastoreen el rebaño de Dios entre ustedes, velando por él, no por obligación, sino voluntariamente, como _quiere_ Dios; no por la avaricia del dinero, sino con sincero deseo; <br ><span class="author">1 Pedro 5:2</span>


>   Les exhortamos, hermanos, a que amonesten a los indisciplinados, animen a los desalentados, sostengan a los débiles _y_ sean pacientes con todos.<br > <span class="author">1 Tesalonicenses 5:14</span>


### ¿Quién falto el domingo?
```dataview
TABLE
   sit-24-12-29 AS "Situación",
   seg-24-12-29 AS "Acciones de seguimiento"
FROM "Personas/Personas" AND #Personas
where sundaygroup = "adultos" AND relation != [[ausentes]] AND relation != [[Visitantes nuevos]] AND relation != [[Visitantes ocasionales]] AND att-24-12-29 != true 
SORT gender ASC
SORT familia ASC
```

### Personas con situaciones de cuidado
```dataview
TABLE 
   sit-24-12-29 AS "Situación", 
   seg-24-12-29 AS "Acciones de seguimiento"
FROM "Personas/Personas" AND #Personas
where sundaygroup = "adultos" AND concern = true AND relation != [[ausentes]]
SORT gender ASC
SORT familia ASC
```

### Desconectados
```dataview
TABLE  sit-24-12-29 AS Situación, seg-24-12-29 AS Seguimiento
FROM "Personas/Personas" AND #Personas
where sundaygroup = "adultos" AND  relation = [[desconectado]]
SORT familia ASC
```

### Nuevos contactos
```dataview
TABLE seguimiento-2023-10-29 AS seguimiento
FROM "Personas/Personas" AND #Personas
where relation = [[Visitantes nuevos]]
SORT tag ASC 
```

### Todos los adultos
```dataview
TABLE seguimiento-2023-10-29 AS seguimiento
FROM "Personas/Personas" AND #Personas
where relation != [[ausentes]] AND sundaygroup = "adultos"
SORT gender ASC
SORT familia ASC
```


### Ausentes
```dataview
TABLE  sit-24-12-29 AS Situación, seg-24-12-29 AS Seguimiento
FROM "Personas/Personas" AND #Personas
where sundaygroup = "adultos" AND  relation = [[ausentes]]
SORT familia ASC
```

```dataview
table
FROM [[]]
```

