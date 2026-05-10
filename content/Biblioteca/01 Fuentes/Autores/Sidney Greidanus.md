---
publish: true
type: author
---
#Biblioteca/Autores

___
### Breve información biográfica
(1935 - )

![[Pasted image 20230401084801.png]]


---


### Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(autor,"[[Sidney Greidanus]]")
sort start asc
```



