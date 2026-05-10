---
publish: true
type: author
---
#Biblioteca/Autores

___
# Breve información biográfica

![Miguel Nuñez|150](https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Pastormn.jpg/220px-Pastormn.jpg)

Miguel Núñez (Santo Domingo, República Dominicana, 5 de julio de 1958) es un médico, teólogo, predicador, misionero, escritor, erudito bíblico y pastor bautista reformado dominicano-estadounidense de Wisdom & Integrity Ministries.

---
# Libros leídos
```dataview
TABLE start AS "Inicio de lectura" FROM #Biblioteca/Libros 
WHERE type = "book" AND contains(author,"Miguel Núñez")
sort start asc
```



