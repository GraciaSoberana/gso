---
publish: true
banner: Files/banners/tasks.jpg
sticker: lucide//chevron-down-square
type: program
fullname: Planeacion Escuela Dominical 2024
date: 2023-11-01
urgency: false
due: 2023-11-30
done: true
related:
  - "[[Instituto de formación cristiana.afdesign]]"
link: 
status: completado
tags:
  - Tasks
important: true
progress: 100
area: "[[Ministerio de discipulado]]"
---
# [[Centro de formación cristiana]]

## Introducción

### Necesidad
Durante el año 2023 pudimos ver la gracia de Dios de muchas maneras en nuestra iglesia local. Nuevos ministerios de discipulado y evangelismo están brotando de manera orgánica. Alabamos a Dios, porque somos conscientes de que que esto es simplemente obra suya. Sin embargo, las nuevas necesidades de nuestra iglesia nos recuerdan que necesitamos contar con creyentes que están creciendo en su amor por Cristo y su palabra, mientras son capacitados con las herramientas bíblicas y teológicas necesarias para realizar su ministerio.


### Objetivos
Nuestra iglesia local tiene la urgente necesidad hombres y mujeres que busquen el rostro de Dios todos los días para reflejar su gloria (Ex. 34:29), que estén  capacitados para usar con eficacia la palabra de verdad (2 Ti. 2:15), y llenos del Espíritu Santo. El [[Centro de formación cristiana]] se ha creado para proporcionar al liderazgo local un entrenamiento bíblico/teológico integral, que proporcione las herramientas para ejercer su ministerio con excelencia.
- Ayudar a nuestros servidores y membresía a entender y vivir la centralidad del evangelio para la vida y servicio cristiano.
- Ayudar los creyentes a tener una panorama claro de la historia de la Biblia.
- Proporcionar un panorama de las principales doctrinas bíblicas.
- Proporcionar herramientas que ayuden a los hermanos a llenarse de la Escritura, vivirla y compartirla con otros.


## Metodología

### Materias
Al diciembre de 2023, esperamos ofrecer cursos en 4 áreas: Santificación personal, Biblia y teología bíblica, Teología sistemática y Capacitación ministerial, con un promedio de 5 cursos al año. 

### Horarios y formatos
Cada materia se impartirá en una modalidad de curso con una duración aproximada de entre 8 y 12 sesiones. Los cursos se realizarán según calendario en diversos horarios y formatos, que pueden ser los siguientes:
- Escuela dominical 10:00 a 10:40 AM. 
- Conferencias semestrales especiales especiales 
- Curso en linea^[Planeado para el segundo semestre de 2024]

### Módulos
Hemos diseñado el [[Centro de formación cristiana]] para impartirse en tres módulos de un año de duración cada uno.  

#### Módulo 1:  Panorama general
Como su nombre lo indica, este módulo está diseñado para ofrecer un panorama general de las Escrituras, la teología, y la centralidad del evangelio. Se espera que todos los creyentes involucrados en ministerios de enseñanza tomen este nivel. 

```dataview
TABLE WITHOUT ID
  clave AS "\#",
  file.link AS "Materia",
  sesiones AS "Duración (hrs)",
  area AS "Área",
  formato AS "Formato"
FROM #Ministerial/Discipulado 
WHERE type = "subject" AND audience = [[]] AND sequence = 1
SORT clave ASC
```
 
#### Modulo 2: Antiguo Testamento y Teología
```dataview
TABLE WITHOUT ID
  clave AS "\#",
  file.link AS "Materia",
  sesiones AS "Duración (hrs)",
  area AS "Área",
  formato AS "Formato"
FROM #Ministerial/Discipulado 
WHERE type = "subject" AND audience = [[]] AND sequence = 2
SORT clave ASC
SORT area DESC
```
 
#### Modulo 3: Nuevo Testamento, teología y Ministerio
```dataview
TABLE WITHOUT ID
  clave AS "\#",
  file.link AS "Materia",
  sesiones AS "Duración (hrs)",
  area AS "Área",
  formato AS "Formato"
FROM #Ministerial/Discipulado 
WHERE type = "subject" AND audience = [[]] AND sequence = 3
SORT clave ASC
```

## Calendario 2024
```dataview
TABLE WITHOUT ID
  clave AS "\#",
  file.link AS "Materia",
  area AS "Área",
  date AS "Fecha", 
  sesiones AS "Sesiones"
FROM #Ministerial/Discipulado 
WHERE type = "subject" AND audience = [[]] AND date < (date(2024-12-12)) 
SORT start ASC
```

