

## Respuestas a las preguntas orientadoras de la cátedra

### ¿Qué ventajas tienen las estructuras elegidas para almacenar los datos de las columnas y roles con respecto a otras de las vistas en la teoría?
En la teoría vimos las diferentes colecciones que se pueden utilizar en Python. A la hora de cargar la información de las columnas, me decanté por utilizar un diccionario que guarde como clave cada una de estas columnas y como valor guarde otro diccionario, donde tenga el tipo de dato y su completitud (Diccionario de Diccionarios). Lo mismo hice con los roles, donde utilicé otro diccionario de diccionarios: la clave va a ser el rol y como valor tengo un diccionario por rol.

La gran ventaja que le encontré frente a usar listas o tuplas es que puedo acceder directo por nombre: si quiero ver los datos de `EDAD`, hago `columnas_eph["EDAD"]` y listo en una sola línea. Si usaba una lista de diccionarios, cada vez que un rol me pedía una columna tenía que armar un `for` para buscarla una por una. Además, con tuplas o listas tendría que acordarme qué posición numérica era cada dato (por ejemplo `[0]` para tipo y `[1]` para porcentaje), lo que hace que el código sea re incómodo de leer y fácil de romper. Con las claves `"tipo"` y `"completitud"` queda todo claro y además el diccionario no me deja repetir columnas ni roles por error. Sumado a eso en caso de tener que agregar alguna que otra columna, es posible y mucho mas facil.



### ¿Qué valores elegiste para los roles y los porcentajes de completitud y por qué?
Al principio tenía la duda de si hacía falta usar `random` para que genere los porcentajes al azar a la hora de correr el programa, pero me di cuenta de que no es necesario y que poner valores fijos dados por mí es mucho mejor para que las pruebas sean controladas y predecibles (si fueran con random, cada vez que corro una celda me darían números distintos y sería un lío).

Para definir los porcentajes a mano me basé lo que se suele completar siempre en una encuesta de este estilo
* A las variables generales y demográficas que se le preguntan a todo el mundo (como `EDAD`, `ANO4`, `REGION`, `TRIMESTRE`, `PONDERA`) les puse **100%** de completitud porque se registran siempre.
* A variables que solo responde una parte de la población (como `CAT_OCUP`, que solo la responde la gente ocupada) le puse **64.5%**.
* A variables donde suele haber ingresos no declarados (como `ITF` o `GDECCFR`) les puse entre **85% y 88%**.

Sumado a eso quise hacerlo variado, porque si les pongo a todos el mismo porcentaje el ejercicio no tiene sentido a la hora de probarlo.

---

### ¿Cómo garantizaste que el programa pueda ser validado con diferentes roles, criterios de ordenamiento y umbrales?
Lo garanticé configurando a propósito a cada uno de los 3 roles con combinaciones bien distintas para probar todos los caminos:
* Al **docente** le puse orden por **completitud** y de forma **descendente (B)**, con un umbral de 70% para probar que el filtro numérico funcione de mayor a menor.
* Al **investigador** le puse orden por **nombre** y de forma **ascendente (A)**, con un umbral más alto (80%) para probar orden alfabético y ver que efectivamente descarte columnas que no llegaban a ese porcentaje (como `CAT_OCUP` que tiene 64.5%).
* Al **analista** le puse orden por **completitud** y **ascendente (A)**, pero con `completitud_minima: None` para validar que cuando un rol no tiene umbral el programa no se rompa y muestre todas sus columnas de interés.

---

### ¿Por qué conviene separar la configuración de los roles (ROLES) de la lógica que genera el informe?
Porque son cosas totalmente distintas: los roles son datos de configuración y las funciones son la lógica. 

Si se me pide agregar un rol nuevo o cambiarle las columnas que mira el docente, solo tengo que modificar dos líneas en el diccionario `tipos_roles`. No tengo que tocar ni una sola línea de las funciones que filtran, ordenan o imprimen. Si tuviera todo mezclado con un montón de `if` metidos adentro de la función, cada vez que quiera cambiar un rol tendría que reescribir código y podría romper cosas que ya andaban bien.

---

### ¿Qué parámetros se pueden definir con valores por defecto?
En mi función `generar_informe(rol=None)` le puse a `rol` el valor por defecto `None`. De esa forma, si alguien llama a la función sin pasarle nada (`generar_informe()`), el programa ya sabe que tiene que mostrar el informe general con todas las columnas ordenadas por completitud descendente. 

También en `filtrar_por_completitud(columnas, minimo=None)` dejé `minimo=None` por defecto, por si alguna vez quiero llamar al filtro sin poner ningún umbral y que me devuelva la lista completa.

---

### Si agregás una nueva columna al dataset, ¿en qué partes del código impacta? ¿Y si solo se quiere que un rol existente incluya esa nueva columna?
* **Si agrego una nueva columna al dataset:** Solo tengo que agregar una línea en el diccionario `columnas_eph` con su tipo y su porcentaje. No toco nada más del código, cuando corra el caso por defecto (sin rol), la nueva columna ya va a salir automáticamente en el listado general ordenada donde le toque.
* **Si quiero que un rol existente la incluya:** Solo tengo que escribir el nombre de esa columna adentro de la lista `"columnas_de_interes"` del rol en el diccionario `tipos_roles`. La función de filtrado y ordenamiento ya se encarga del resto sola.

---

### ¿Qué pasaría si un rol tuviera un criterio de orden distinto a los especificados "nombre" o "completitud" (por ejemplo, "promedio")? ¿Cómo lo detectarías y qué harías para que el programa no falle?
En mi código, como uso un `if criterio == "completitud": ... else:`, si alguien escribe "promedio" caería en el `else` y ordenaría por nombre por descarte. 

Para detectarlo y que quede más prolijo, podría poner una validación antes de ordenar de que si no es ninguno de esos criterios, tambien ordene o diga que no es el criterio adecuado

---

### ¿Qué cambiarías si por defecto se pide que el informe deba salir según uno de los roles?
Si me pidieran que al no poner rol salga por defecto el informe del docente, en la definición de la función cambiaría el valor por defecto a `rol="docente"` por ejemplo. O adentro del código, si veo que no ingresó nada, hago `rol = "docente"`. Con ese único cambio el programa reutiliza y no tengo que duplicar nada

---

## 2. Aclaraciones post clase del 23/09 sobre la bitacora

En esta bitácora respondí las preguntas orientadoras planteadas por la cátedra para dejar registro de cómo fui pensando y construyendo el programa. En la clase del miércoles pude terminar de comprender qué es lambda, cómo aplicarlo de forma óptima en el código y cómo contemplar el caso en el que se ingrese por teclado un rol que no esté cargado en el diccionario.

Hablando con los profesores, me aconsejaron dejar constancia en la bitácora de los momentos en que recurrí a la inteligencia artificial. Mi intención fue mantener su uso lo más reducido posible, mas que nada lo utilice para la comprensión de lambda, al no tenerlo tan practicado, me costó integrarlo por mi cuenta dentro del ordenamiento, por lo que usé la IA para destrabar la sintaxis y terminar de asimilar el concepto junto con el material de teoría y lo visto en clase. Por ultimo, para el formato visual de salida, me ayudó con la parte estética al momento de imprimir los resultados en la terminal, ya que en mis primeros intentos las columnas quedaban desfasadas y poco legibles al mostrarlas en pantalla.
