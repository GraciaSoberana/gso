---
publish: true
type: series
area: "[[Ministerio de predicación]]"
start: 2023-08-06
end: 2023-12-03
related:
  - "[[Efesios]]"
tags:
  - Sermones
---

[[Series de sermones]] basada en| la Epístola de Pablo a los  [[Efesios]], Predicada en Gracia Soberana Orizaba en Agosto - Noviembre 2023

```dataview
TABLE WITHOUT ID sequence AS " ", file.link AS "Título", passage AS "Base bíblica", preacher AS "Predicador", date AS "Fecha"
FROM #Sermones
WHERE type = "sermon" AND series = [[]]
SORT sequence ASC
```

```dataview
calendar date
FROM #Sermones/Efesios
WHERE type = "sermon"
```
