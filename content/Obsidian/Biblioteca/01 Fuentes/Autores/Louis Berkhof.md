---
publish: true
type: author
---
#Biblioteca/Autores

___
# Breve información biográfica

![[Pasted image 20230329220815.png|300]]


---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(autor,"[[Louis Berkhof]]")
sort start asc
```



