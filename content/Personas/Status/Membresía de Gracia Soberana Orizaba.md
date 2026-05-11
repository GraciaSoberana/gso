---
type: admin
related:
  - "[[Gracia Soberana Orizaba]]"
  - "[[Personas en Gracia Soberana Orizaba]]"
---

Lista de membresía de  Gracia Soberana Orizaba

```dataview
TABLE familia AS "Familia", phone AS "Teléfono", GrupoDemográfico AS "Estado civil"
FROM #Personas
WHERE type="persona" AND relation = [[]]
SORT  familia
```
