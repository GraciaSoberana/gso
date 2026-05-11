---
publish: true
type: series
area: "[[Ministerio de predicación]]"
date: 2024-01-01
due: 2024-04-21
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
  - "[[Dieta de predicaciones 2026]]"
progress: 5
sticker: lucide//clipboard-list
start:
banner: Sermones/Compromisos de Gracia/images/banner -compromisos.jpg
end:
passage: "[[Espíritu Santo]]"
---

```dataview
TABLE WITHOUT ID sequence AS " ", file.link AS "Título", passage AS "Tópico", date AS "Fecha"
FROM #Sermones AND !"Templates"
WHERE type = "sermon" AND series = [[]]
SORT sequence ASC
```

