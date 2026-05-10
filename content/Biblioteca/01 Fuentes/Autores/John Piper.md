---
publish: true
---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(author,"John Piper")
sort start asc
```
