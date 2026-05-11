---
publish: true
type: Canal de Youtube
---
#Biblioteca/Autores

___
# Breve información biográfica

![Autor|150](https://)



---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(autor,"[[Full of eyes]]")
sort start asc
```



