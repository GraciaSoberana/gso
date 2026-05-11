---
publish: true
type: series
area: "[[Ministerio de predicación]]"
date: 2024-01-01
tags:
  - Sermones
  - Series
related:
  - "[[Series de sermones]]"
  - "[[Dieta de predicaciones 2026]]"
  - "[[Apocalipsis|Apocalipsis]]"
start: 2024-03-31
end:
---
 ![[Apocalipsis-cover.jpg|banner]]
## Presentacion
Imagina que estamos en una película épica. La trama se desarrolla en un mundo lleno de desafíos, persecución, dolor y muerte. La Iglesia de Cristo es el personaje principal, y nosotros somos parte de ella. Hay enemigos aterradores y poderosos que hacen guerra contra ella. A veces nos sentimos abrumados porque parece que los enemigos van a vencer y pensamos que no podremos seguir soportando esta tribulación. Pero aquí está la clave: el Director de esta película es Jesucristo. Él tiene el guion completo en sus manos. Sabe cómo terminará todo. Y lo mejor de todo es que ¡ya hemos leído el final! Sabemos que al final, el bien vencerá al mal, la luz disipará las tinieblas y el Cordero reinará para siempre.

En esta película, hay momentos de tensión, pero también hay momentos de esperanza. Jesús nos llama a permanecer fieles, incluso cuando las cosas se ponen difíciles. Nos invita a confiar en que Él está tejiendo cada detalle para nuestro bien. A veces, la persecución puede parecer abrumadora, pero recordamos que Jesús ya venció a sus enemigos. Y aunque enfrentemos enfermedades, dolor y pérdidas, sabemos que hay un gozo eterno esperándonos al final.

Así que, en medio de esta gran aventura, seguimos luchando, sufriendo, amando, perdonando y compartiendo el evangelio. Porque sabemos que, al final, la pantalla se iluminará con la gloria de Dios, y todos los créditos irán a nuestro Salvador. ¡Esperamos ese día con ansias!"

## Calendario
Basados en esta [[Estructura de Apocalipsis]], se propone el siguiente calendario provisional

```dataview
TABLE WITHOUT ID sequence AS " ", file.link AS "Título", passage AS "Tópico", date AS "Fecha"
FROM #Sermones AND !"Templates"
WHERE type = "sermon" AND series = [[]]
SORT sequence ASC
```

## Alabanzas


```dataview
Table choice(ready,"✅","❌") AS "Cantada", link
FROM #songs 
WHERE contains(related,[[]])
SORT ready DESC
```

## Videos complementarios
```dataview
TABLE WITHOUT ID sequence AS " ", file.link AS "Título", passage AS "Tópico", date AS "Fecha"
FROM #Videos AND !"Templates"
WHERE type = "video" AND series = [[]]
SORT sequence ASC
```
