---
publish: true
type: series
area: "[[Ministerio de predicación]]"
date: 2024-02-16
tags:
  - Sermones
  - Series
  - Tasks
related:
  - "[[Talleres de matrimonios]]"
  - "[[Para servir necesitamos crecer]]"
files:
  - "[[Amando como Cristo.afdesign]]"
done: true
---

```dataview
TABLE WITHOUT ID 
  sequence AS " ", 
  file.link AS "Título", 
  topic AS "Tópico", 
  date AS "Fecha",
  slides AS "Slides",
  audio AS "Audio"
FROM #Sermones 
WHERE type = "sermon" AND series = [[]]
SORT sequence ASC
```
 