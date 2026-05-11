Reporte de asistencia a [[Gracia Soberana Orizaba]] de las 
[[Personas en Gracia Soberana Orizaba]]

```dataview
TABLE  choice(asistencia-2023-10-01,"✅","❌") AS "10/01", choice(asistencia-2023-10-08,"✅","❌") AS "10/08", choice(asistencia-2023-10-15,"✅","❌") AS "10/15", choice(asistencia-2023-10-22,"✅","❌") AS "10/22", choice(asistencia-2023-10-29,"✅","❌") AS "10/29"
FROM #Personas AND "Personas/Personas"
WHERE type = "persona" AND status != [[ausentes]]  AND status != [[Visitantes]]  AND sundaygroup = "adultos"
SORT name ASC
```




