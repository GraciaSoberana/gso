---
publish: true
type: author
---
#Biblioteca/Autores

___
# Breve información biográfica

![Autor](https://upload.wikimedia.org/wikipedia/commons/1/14/Geerhardus_Johannes_Vos_%281862%E2%80%931949%29.jpg)

---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(autor,"[[Geerhardus Vos]]")
sort start asc
```



