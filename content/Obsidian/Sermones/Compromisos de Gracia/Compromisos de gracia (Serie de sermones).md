---
publish: true
type: series
area: "[[Ministerio de predicación]]"
date: 2024-01-01
due: 2023-12-31
urgency: true
important: true
done: true
status: completado
tags:
  - Sermones
  - Series
  - Tasks
related:
  - "[[Series de sermones]]"
  - "[[Dieta de predicaciones 2026]]"
progress: 100
sticker: lucide//clipboard-list
start: 2024-01-07
banner: Sermones/Compromisos de Gracia/images/compromisos de Gracia - banner.jpg
end: 2024-02-25
passage: "[[Señorío de Cristo]]"
files: "[[Compromisos de Gracia.afdesign]]"
---

```dataview
TABLE WITHOUT ID 
  sequence AS " ", 
  file.link AS "Título", 
  passage AS "Tópico", 
  date AS "Fecha",
  slides AS "Slides",
  audio AS "Audio"
FROM #Sermones AND !"Templates"
WHERE type = "sermon" AND series = [[]]
SORT sequence ASC
```

 arte: [[Compromisos de Gracia.afdesign]]
