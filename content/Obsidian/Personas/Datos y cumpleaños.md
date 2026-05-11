---
type: admin
area: pastoral
---

### Adultos constantes
``` dataview
TABLE  
  dateformat(birthdate, "dd/MM") AS Cumpleaños, 
  familia
FROM #Personas
WHERE 
  type = "persona" AND 
  relation != [[ausentes]] AND
  relation != "template" AND
  relation != [[menor]] AND
  relation != [[Visitantes ocasionales]] 
SORT familia ASC
```

### Visitantes
``` dataview
TABLE  
  dateformat(birthdate, "dd/MM") AS Cumpleaños, 
  familia
FROM #Personas
WHERE 
  type = "persona" AND 
  relation = [[Visitantes ocasionales]] 
SORT familia ASC
```

### Menores
``` dataview
TABLE  
  dateformat(birthdate, "dd/MM") AS Cumpleaños, 
  familia
FROM #Personas
WHERE 
  type = "persona" AND 
  relation != "template" AND
  relation = [[menor]] 
SORT familia ASC
```

