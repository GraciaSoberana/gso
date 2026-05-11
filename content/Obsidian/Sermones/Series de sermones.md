---
publish: true
type: program
---

Series de sermones predicados en [[Gracia Soberana Orizaba]], 


```dataview
TABLE
start AS "Inicio", end AS "Final"
FROM #Sermones 
WHERE type = "series"
SORT start DESC
```
