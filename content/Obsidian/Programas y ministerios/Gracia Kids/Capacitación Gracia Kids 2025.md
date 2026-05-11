---
publish: true
banner: Files/banners/tasks.jpg
sticker: lucide//chevron-down-square
type: program
area: "[[Capacitación de servidores 2026]]"
aliases:
date: 2023-11-29
due: 2023-11-29
urgency: false
important: true
done: true
status: completado
related:
  - "[[Gracia Kids y  Gracia Teens]]"
link:
tags:
  - Tasks
progress: 8
files:
  - "[[CapacitacionKids.afdesign]]"
---
Sabemos que la mayoría de nuestros maestros y servidores cuentan con un horario laboral o familiar muy demandante del cual ya están tomando tiempo para preparar las clases. 


Sin embargo, también reconocemos que tenemos una profunda necesidad de crecer como maestros [[Bíblicamente solidos]] y [[Capacitados para enseñar]]. 

Por lo tanto, nuestro programa de capacitación esta planeado para que, de manera progresiva, los maestros vayan creciendo en su conocimiento y habilidades bíblicas, teológicas y técnicas.

### Capacitaciones obligatorias

- [[Plan de lectura cronológico (2024)]]
- Juntas trimestrales
%%
```dataview
TABLE WITHOUT ID
   sequence AS "\#",
   ("[[" + file.name + "|" + title + "]]") AS Evento,
   date AS FECHA
FROM #entrenamiento 
WHERE contains(related, [[]])
SORT date ASC
```
%%

| \#  | Evento                               | Tema                           | Fecha      |
| --- | ------------------------------------ | ------------------------------ | ---------- |
| 1   | Taller de Métodos de estudio bíblico | [[Métodos de estudio bíblico]] | Marzo 25   |
| 2   | [[El gran panorama de la redención]] | [[Teología bíblica]]           | Febrero 25 |
| 3   | [[Nosotros creemos (serie)]]         | [[Teología Sistemática]]       | Mayo 25    |

