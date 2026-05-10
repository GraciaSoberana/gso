---
publish: true
type: author
---
#Biblioteca/Autores

___
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(author,"Iglesias Gracia Soberana")
sort start asc
```



