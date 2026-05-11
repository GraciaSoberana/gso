Personas que asisten con regularidad a [[Gracia Soberana Orizaba]], pero aun no se han hecho miembros

```dataview
TABLE 
   relation AS "Ralación con la iglesia",
   origin AS "Procedencia"
FROM #Personas 
WHERE discipleship = "needed"
SORT origin DESC, familia ASC
```

