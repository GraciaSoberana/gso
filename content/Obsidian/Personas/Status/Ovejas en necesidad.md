Personas que asisten con regularidad a [[Gracia Soberana Orizaba]], pero aun no se han hecho miembros

```dataview
TABLE concernclass AS "Necesidad", familia, lastprayer AS "Orando por"
FROM #Personas AND !#HombresClave 
WHERE concern = true AND relation != [[ausentes]]
SORT gender ASC
SORT familia ASC 
```

