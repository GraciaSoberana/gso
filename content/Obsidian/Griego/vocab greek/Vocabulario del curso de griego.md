---
publish: true
dg-publish: true
updated_at: 2025-02-21T09:40:44.989-06:00
edited_seconds: 180
---


![[greektext.jpg|banner]]



- [[Vocabulario completo]]
- [[Sustantivos de 3a declinación]]

```base
filters:
  and:
    - type == "greekwordNT"
    - "!morfologia.isEmpty()"
    - clase <= 11
views:
  - type: table
    name: Verbos
    filters:
      and:
        - morfologia.contains("Verbo")
        - aoristo2do.isEmpty()
    order:
      - file.name
      - clase
      - morfologia
      - frecuencia
    sort:
      - property: clase
        direction: ASC
      - property: frecuencia
        direction: DESC
  - type: table
    name: Sustantivos masculinos
    filters:
      and:
        - or:
            - morfologia == "Sustantivo 2a declinación masculino"
            - morfologia == "Sustantivo 2a declinación neutro"
            - morfologia == "Sustantivo 2a declinación femenino"
            - morfologia == "Sustantivo femenino 2a declinación"
    order:
      - file.name
      - clase
      - morfologia
      - frecuencia
    sort:
      - property: frecuencia
        direction: DESC
    columnSize:
      note.morfologia: 345
  - type: table
    name: Todos
    order:
      - palabra
      - traduccion
      - clase
    sort:
      - property: clase
        direction: ASC
      - property: frecuencia
        direction: DESC
    columnSize:
      note.palabra: 201
  - type: table
    name: Sustantivos 3a
    filters:
      and:
        - or:
            - morfologia == "Sustantivo 3a declinación"
            - morfologia == "Sustantivo 3a declinación neutro"
            - morfologia == "Sustantivo 3a declinación femenino"
            - morfologia == "Sustantivo 3a declinación masculino"
    order:
      - file.name
      - clase
      - morfologia
      - frecuencia
    sort:
      - property: frecuencia
        direction: DESC
    columnSize:
      note.morfologia: 345
  - type: table
    name: Sustantivos 1a
    filters:
      and:
        - or:
            - morfologia == "Sustantivo 1a declinación femenino"
            - morfologia == "Sustantivo 1a declinación masculino"
    order:
      - file.name
      - clase
      - morfologia
      - frecuencia
    sort:
      - property: frecuencia
        direction: DESC

```

### Espe

```dataview
TABLE WITHOUT ID
  file.link AS "Título",
  traduccion,
  clase
WHERE 
  type = "greekwordNT" AND  clase >= 1 AND clase <= 13 
SORT clase ASC
```


1. **[[καί]]**: y, también, entonces, pero
2. **[[οὐ 1|οὐ, οὐκ, οὐχ]]**: no
3. **[[λέγω]]**: decir, llamar 
 4. **[[θεός]]**: Dios
 5. **[[Ἰησοῦς]]**: Jesús
 6. **[[ἔχω]]**: tener, necesitar
 7. **[[ἀκούω]]**: oír, escuchar
 8. **[[λαμβάνω]]**: tomar, recibir 
 9. **[[πιστεύω]]**: querer, desear
 10. **[[γινώσκω]]**: saber, aprender, entender, reconocer 
 11. **[[θέλω]]**: desear, querer 
 12. **[[γράφω]]**: escribir 
 13. **[[εὑρίσκω]]**: hallar; encontrar
 14. **[[ἐσθίω]]**: comer 
 15. **[[ἐγείρω]]**: resucitar; levantarse
 16. **[[ἀποστέλλω]]**: enviar
 17. **[[βλέπω]]**: ver, mirar 
 18. **[[βάλλω]]**: arrojar, echar 
 19. **[[μένω]]**: permanecer, quedar, morar
 20. **[[λύω]]**: desatar; destruir, liberar
21. [[κύριος]]: Señor; señor; dueño
22. [[ἄνθρωπος]]: hombre
23. [[Χριστός]]: Cristo
24. [[υἱός]]: hijo
25. [[ἀδελφός]]: hermano
26. [[λόγος]]: palabra
27. [[οὐρανός]]: cielo 
28. [[Ἰουδαῖος]]: judío; 
29. [[νόμος]]: ley 
30. [[κόσμος]]: mundo; adorno 
31. [[ἄγγελος]]: ángel; mensajero 
32. [[ὄχλος]]: muchedumbre; multitud; gente 
33. [[ἔργον]]: obra; acción
34. [[δοῦλος]]: siervo; esclavo
35. [[θάνατος]]: muerte
36. [[ὀφθαλμός]]: ojo, vista
37. [[τέκνον]]: hijo; niño 
38. [[ἄρτος]]: pan
39. [[καιρός]]: tiempo; debido tiempo, oportunidad
40. [[θηρίον]]: bestia; animal; fiera
41. [[γίνομαι]]: suceder; ser; ser hecho
42. [[παραγίνομαι]]: llegar, venir, presentarse
43. [[ἔρχομαι]]: ir; venir; llegar
44. [[ἐξέρχομαι]]: salir; ir afuera
45. [[εἰσέρχομαι]]: entrar
46. [[διέρχομαι]]: Pasar; atravesar
47. [[συνέρχομαι]]: reunirse; acompañar
48. [[παρέρχομαι]]: pasar
49. [[προσέρχομαι]]: acercarse; llegar
50. [[ἀποκρίνομαι]]: responder
51. [[δύναμαι]]: ser apto; poder
52. [[πορεύομαι]]: ir; venir
53. [[ἀπέρχομαι]]: irse; partir
54. [[κάθημαι]]: sentarse; montar (a caballo); residir
55. [[προσεύχομαι]]: orar
56. [[ἀσπάζομαι]]: saludar; dar la bienvenida
57. [[δέχομαι]]: Recibir; aceptar
58. [[λογίζομαι]]: considerar; pensar
59. [[βούλομαι]]: querer
60. [[καυχάομαι]]: gloriarse; jactarse
61. [[ἐργάζομαι]]: trabajar; hacer; obrar
62. **[[ἐν]] + dativo:** en
63. **[[εἰς 1|εἰς]] + acusativo:** a; hacia
64. **[[ἐκ]] + genitivo:** de; fuera de
65. **[[ἐπί]] + genitivo:** sobre
66. **[[ἐπί]] + dativo:** encima de
67. **[[ἐπί]] + acusativo:** en, contra, por
68. **[[πρός]] + acusativo:** hacia
69. **[[διά]] + genitivo:** a través de
70. **[[διά]] + acusativo:** a causa de
71. **[[ἀπό 1|ἀπό]] + genitivo:** de, desde
72. **[[κατά]] + genitivo:** contra
73. **[[κατά]] + acusativo:** según.
74. **[[μετά]] + acusativo:** después de, 
75. **[[μετά]] + genitivo:** en, contra, por
76. **[[περί]] + genitivo:** acerca de
77. **[[περί]] + acusativo:** alrededor de
78. **[[ὑπό]] + genitivo:** por; bajo; debajo; 
79. **[[ὑπό]] + genitivo:** por, por medio de, 
80. **[[ὑπό]] + acusativo:** debajo de
81. **[[παρά]] + genitivo:**  De, de parte de, por
82. **[[παρά]] + dativo:** con
83. **[[παρά]] + acusativo:** Junto a, a lo largo de
84. **[[ὑπέρ]] + genitivo**: Por, en nombre de, en favor de, 
85. **[[ὑπέρ]] + acusativo**: Más allá de, más que, por encima de
86. **[[σύν]] + dativo**(Nosotros) nos ibamos****: con; junto con
87. **[[ἐνώπιον]] + gen**: ante; delante de
88. **[[ἄχρι]] + gen**: hasta
89. **[[ἔμπροσθεν]] + gen**: delante de; al frente de; delante
90. **[[πρό]] + gen**: Ante de; delante de
91. [[ἀναβαίνω]]: subir; ascender
92. [[καταβαίνω]]: descender; bajar
93. [[ἐκβάλλω]]: expulsar, sacar, arrojar
94. [[ἀνοίγω]]: abrir; 
95. [[ἀποκτείνω]]: matar
96. [[ἀπολύω]]: Soltar; divorciarse; repudiar; despedir; perdonar
97. [[συνάγω]]: reunirse; recoger, juntar, recibir
98. [[παραλαμβάνω]]: tomar; recibir; llevar
99. [[προσφέρω]]: : ofrecer; presentar; traer; 
100. [[ἀπαγγέλλω]]: informar; contar; comunicar; avisar
101. [[ἐπιγινώσκω]]: conocer; reconocer; saber
102. [[παρακαλέω]]: Rogar, exhortar, consolar
103. [[περιπατέω]]: andar; caminar
104. **[[ἡμέρα]]**: día
105. **[[μαθητής]]**: discípulo; 
106. **[[γῆ]]**: tierra
107. **[[ἁμαρτία]]**: pecado; 
108. **[[δόξα]]**: gloria; esplendor, majestad
109. **[[βασιλεία]]**: reino
110. **[[καρδία]]**: corazón
111. **[[προφήτης]]**: profeta
112. **[[φωνή]]**: voz; sonido
113. **[[ζωή]]**: vida
114. **[[ἀγάπη]]**: amor
115. **[[ἐκκλησία]]**: iglesia
116. **[[ἀλήθεια]]**: verdad
117. **[[ὥρα]]**: hora
118. **[[ἐξουσία]]**: autoridad; poder
119. **[[ἀρχή]]**: principio; comienzo, principado; gobernante
120. **[[ψυχή]]**: vida; alma; persona
121. **[[οἰκία]]**: casa
122. **[[δικαιοσύνη]]**: justicia
123. **[[εἰρήνη]]**: paz
124. **ἡ [[ὁδός]]**: Camino  
125. **[[εἰμί]]**: ser; estar; haber  
126. **[[ἐγώ]]**: yo  
127. **[[σύ]]**: tú  
128. **[[αὐτός]]**: él  
129. **[[ἐγώ|ἡμεῖς]]**: Nosotros  
130. **[[σύ|ὑμεῖς]]**: Vosotros; ustedes  
131. **[[οὗτος]]**: este  
132. **[[δὲ]]**: pero; y; entonces  
133. **[[ὅτι]]**: que; porque; “”  
134. **[[γάρ]]**: porque; pues  
135. **[[ἀλλά]]**: Sino; pero; sin embargo  
136. **[[ἐκεῖνος]]**: ese; aquel; Él  
137. **[[Παῦλος]]**: Pablo  
138. **[[Πέτρος]]**: Pedro  
139. **[[λαός]]**: pueblo; gente  
140. **[[Ἰωάννης]]**: Juan  
141. **[[οἶκος]]**: casa  
142. **[[ἀποθνῄσκω]]**: morir; perecer  
143. **[[αἴρω]]**: tomar; quitar; llevar  
144. [[ἅγιος]]: santo;
145. [[πρῶτος]]: primero
146. [[ἄλλος]]: otro;
147. [[νεκρός]]: muerte;
148. [[μόνος]]: solo; solamente
149. [[ἴδιος]]: propio; suyo, su propio
150. [[ὅλος]]: todo; entero; completo
151. [[ἀγαθός]]: bueno (ético)
152. [[καλός]]: bueno (estético)
153. [[ἕτερος]]: otro;
154. [[δίκαιος]]: justo; inocente
155. [[πονηρός]]: Mal; maligno; perverso;
156. [[αἰώνιος]]: eterno
157. [[πιστός]]: fiel; creyente
158. [[ἀγαπητός]]: amado; querido
159. [[κρίνω]]: juzgar; decidir; condenar
160. [[ἀποθνῄσκω]]: morir; perecer
161. [[μέλλω]]: ir a, estar a punto de
162. [[σῴζω]]: salvar; sanar
163. [[αἴρω]]: tomar; quitar; llevar
164. [[ὀφθαλμός]]: ojo, vista
165. [[ὑπάγω]]: venir, ir, quitar
166. [[χαίρω]]: regocijar; alegrarse
167. [[πίνω]]: beber
168. [[ἄγω]]: llevar; traer;
169. [φέρω]]: llevar; traer
170. [[ἁμαρτάνω]]: pecar
171. [[πάσχω]]: sufrir; padecer
172. [[ἐργάζομαι]]: trabajar; hacer; obrar
173. [[βούλομαι]]: querer, ser su voluntad
174. [[καυχάομαι]]: gloriarse; jactarse
175. [[ἀναγινώσκω]]: leer;
176. - [[καθώς]]: como, cómo, tal como, así como
177. [[μέν]]: ciertamente; verdad; uno (distributivo)
178. [[νῦν]]: ahora
179. [[οὐδείς]]: nadie; nada; ninguno; no
180. [[οὖν]]: Entonces; Por tanto, Pues, así que
181. [[πάλιν]]: otra vez, de nuevo, también
182. [[πῶς]]: ¿cómo?; que, qué; por qué
183. [[τέ]]: y; tanto; también
184. [[τότε]]: entonces; luego; en aquel tiempo
185. [[ἀμήν]]: En verdad; Amén, verdad, De cierto
186. [[ἤ 1|ἤ]]: o; que;
187. [[ὅτε]]: cuando
188. [[ὡς]]: como; cómo; Cuando
189. [[δει]]: deber, es necesario, tener
190. [[διδάσκω]]: enseñar
191. [[κἀγώ]]: y yo, yo también
192. [[οὐδέ]]: y no; ni, tampoco
193. [[οὔτε]]: ni, no, tampoco
194. [[πίπτω]]: caer; postrarse
195. [[σός]]: tu; tus
196. [[σεαυτοῦ]]: tú mismo
197. [[τίς]]: ¿quién?; ¿qué?
198. [[τὶς]]: alguien; alguno; algo
199. [[ἀλλήλων]]: unos a otros
200. [[ἄρχω]]: comenzar; regir
201. [[ἐμαυτοῦ]]: Yo mismo, me
202. [[ἐμός]]: mi; mío
203. [[ἑαυτοῦ]]: sí mismo; sí misma; de él; de ella
204. [[ὅστις]]: que, cual, cualquiera
205. [[ὅταν]]: cuando
206. [[ὅς 1|ὅς]]: que; quien; cual




