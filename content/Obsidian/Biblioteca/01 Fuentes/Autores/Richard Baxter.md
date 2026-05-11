---
publish: true
type: author
---
#Biblioteca/Autores

# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND author = "[[Richard Baxter]]"
sort start asc
```



