---
publish: true
type: author
---
#Biblioteca/Autores

___
# Breve información biográfica

![Autor|150](https://cdn.shopify.com/s/files/1/0021/5210/3983/collections/Ferguson.png)


---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(author,"Sinclair Ferguson")
sort start asc
```



