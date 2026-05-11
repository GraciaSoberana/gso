Personas que asisten con regularidad a [[Gracia Soberana Orizaba]], pero aun no se han hecho miembros

```dataview
TABLE familia AS "Familia", phone AS "Teléfono", GrupoDemográfico AS "Estado civil"
FROM #Personas 
WHERE relation = [[]]
SORT familia ASC
```

