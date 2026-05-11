---
publish: true
dg-publish: true
updated_at: 2025-02-21T09:40:44.989-06:00
edited_seconds: 180
---

![[greektext.jpg|banner]]





```dataview
TABLE
traduccion, frecuencia
WHERE 
  type = "greekwordNT" AND contains(morfologia, "μι") and clase > 0 and clase < 29
SORT frecuencia desc
```
