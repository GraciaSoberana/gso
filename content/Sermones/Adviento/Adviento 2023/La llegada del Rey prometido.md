---
publish: true
type: series
banner: Sermones/Adviento 2023/images/adviento 23 banner.jpg
area: "[[Ministerio de predicación]]"
start: 2023-12-10
end: 2023-12-31
date: 2023-12-05
due: 2023-12-06
urgency: true
important: true
done: true
status: pendiente
tags:
  - Sermones
  - Series
  - Tasks
related:
  - "[[Series de sermones]]"
progress: 100
sticker: lucide//clipboard-list
---

Esta serie de sermones de [[Adviento]] estará basada en los primeros 2 capítulos de Mateo.

```dataview
TABLE WITHOUT ID sequence AS " ", file.link AS "Título", passage AS "Base bíblica", date AS "Fecha"
FROM #Sermones
WHERE type = "sermon" AND series = [[]]
SORT sequence ASC
```

