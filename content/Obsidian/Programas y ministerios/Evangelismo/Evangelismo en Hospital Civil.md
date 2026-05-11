---
publish: true
type: adm
---

#Ministerial/Evangelismo 

Parte de las [[Iniciativas de evangelismo]] como parte de la Iglesia Gracia Soberana Orizaba

![[Logo - evangelismo.png|400]]
### Integrantes del [[Evangelismo en Hospital Civil]]
```dataview 
LIST FROM  #Personas
WHERE contains(ministerio, [[Evangelismo en Hospital Civil]])
```

![[Logo - evangelismo.png|400]]
### <span style='color:#2d98da'>Cronograma</span> <br >Mayo 24
```dataview 
TABLE WITHOUT ID 
   date AS "Fecha", 
   alimentos AS "Pancito", 
   bebida AS "Café", 
   desechables AS "Desechables", 
   mensaje AS "Prédica"
FROM  #Evangelismo/Hospital AND "Eventos"
WHERE date >= date(2024-05-01)
SORT date ASC
```

