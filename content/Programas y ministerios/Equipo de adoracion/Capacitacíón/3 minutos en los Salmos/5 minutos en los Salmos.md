---
publish: true
date: 2023-10-04
banner: Files/banners/salmos.jpg
---
Spots que preparo como parte de la [[Capacitación y planeacion mayo  2026]] de Gracia Soberana Orizaba.

```dataview
TABLE WITHOUT ID sequence AS " ", file.link AS "Título", passage AS "Base bíblica", goal AS Objetivo, date AS "Fecha"
FROM #podcasts/3MS
WHERE type = "podcast" AND date > date(2023-08-01)
SORT sequence ASC
```
