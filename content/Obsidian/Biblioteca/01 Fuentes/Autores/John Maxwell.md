---
publish: true
type: author
tags:
  - Biblioteca/Autores
sticker: lucide//pen-tool
---

# Breve información biográfica

![Autor|150](https://)



---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND autor = [[]]
sort start asc
```



