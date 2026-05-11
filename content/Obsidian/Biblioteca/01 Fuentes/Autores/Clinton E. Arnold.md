---
publish: true
type: author
---
#Biblioteca/Autores

___
# Breve información biográfica

![Autor|150](https://)



---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(autor,"[[Clinton E. Arnold]]")
sort start asc
```



