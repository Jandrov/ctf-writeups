# Write-up BitupCTF

* [Misc - Inosmnia](#misc---insomnia)
* [Web - Fintechno](#web---fintechno)
* [Web - Curvas Peligrosas](#web---curvas-peligrosas)
* [Atomics - Hello World](#atomics---hello-world)
* [Atomics - Demiguise](#atomics---demiguise)
* [Atomics - Hexa](#atomics---hexa)
* [Atomics - Helius 5](#atomics---helius-5)
* [Atomics - Un Ciudadano Ejemplar](#atomics---un-ciudadano-ejemplar)


<p align="center">
  <img src="imgs/scoreboard.png">
</p>


Los miembros de [SQLazo](https://twitter.com/SQLazo) decidimos participar en el CTF del fin de semana pasado organizado por [BitUp Alicante](https://bitupalicante.com/) en el que había buenos premios para los 3 primeros clasificados, buena variedad de retos y donde participaban dos de los tres equipos españoles que nos superan en [CTFTime](https://ctftime.org/stats/ES). Solo pudimos participar 3 miembros de mi equipo pero conseguimos un muy buen 5º puesto, con varios retos que no conseguimos solo por detalles o tonterías. Aquí van algunos writeups:



## Misc - Insomnia

Ficheros: <a href="challs/evil.zip">evil.zip</a>

<p align="center">
  <img src="imgs/misc/insomnia.png">
</p>

En este reto nos dan un fichero comprimido que contiene otro llamado `kdaWvc7exPjKad3.cs`. Comprobando el tipo de archivo con el comando *file* vemos que es ASCII text, pero al abrirlo en un editor como Sublime vemos que en realidad es un script de **PowerShell**. Lo renombramos para que lo reconozca el *Windows PowerShell ISE* y probamos a ejecutarlo. Nos pide introducir la flag, probamos algo y dice que no es correcta. 

<p align="center">
  <img src="imgs/misc/insomnia1.PNG">
</p>

Toca ver el código y tratar de entender qué está ocurriendo. Podemos observar una flag "hardcodeada" cifrada, así que asumo que la introducida por nosotros se cifra en el código y luego se compara con esa. Vemos que el script consta de:
* La flag cifrada
* 4 funciones
* 7 líneas de código
* Un bloque if...else 

El problema de todo esto es que el código parece estar bastante ofuscado, teniendo las variables y funciones nombres muy extraños. Toca entonces renombrarlos con Sublime para tratar de comprender qué hace el código. 
Tras el proceso de *beautify* del script y dándome cuenta de que uno de los valores hardcodeados es *RightToLeft* cifrado (simplemente permite entender mejor que esa función lo que hace es invertir los caracteres), [este es el script resultante](./challs/clean.ps1).

<p align="center">
  <img src="imgs/misc/insomnia2.PNG">
</p>

Ya aquí es sencillo ver que la cuarta función nunca se ejecuta y que el proceso que sigue con lo que introducimos es **base64, fun1 (from base64 + XOR con 0x4c), reverse y base64 otra vez**. Entonces invirtiendo el proceso en [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)Reverse('Character')XOR(%7B'option':'Hex','string':'0x4c'%7D,'Standard',false)&input=TVcxL0lYd2ZLVHNORTM4K2VCTTVmRFUzZkg0OE9UZ2xMZz09) encontramos la flag del reto
 
<p align="center">
  <img src="imgs/misc/insomnia_solution.PNG">
</p>

**bitup20{y0u_4r3_AweS0m3!}**


## Web - Fintechno

Ficheros: <a href="challs/a_sad_song.mp3">a_sad_song.mp3</a>

<p align="center">
  <img src="imgs/web/fintechno.png">
</p>

Examinamos con **file** el fichero que nos dan y resulta no ser un audio sino un texto:

<p align="center">
  <img src="imgs/web/fintechno2.PNG">
</p>

Lo abrimos y vemos una codificación que parece **base64** así que lo metemos en CyberChef. Ahí nos sugiere su herramienta automática que lo que queda es un fichero **SQLite**:

<p align="center">
  <img src="imgs/web/fintechno3.PNG">
</p>

Abrimos el fichero en Kali y vemos varias tablas:

<p align="center">
  <img src="imgs/web/fintechno4.PNG">
</p>

Viendo los registros de cada tabla con la típica query _select * from <tabla>_, nos encontramos con contenido sospechoso en la tabla **moz_places**:

<p align="center">
  <img src="imgs/web/fintechno1.PNG">
</p>

Aquí aparecen las webs del reto (al final la categoría es *Web*). Entramos a explorarlas un poco y tras perder algo el tiempo probando típicas acciones de web, decido ir siguiendo cada uno de los links de *moz_places* en orden, pues veo que aparece **oauth** en el proceso, y quizá se reutilice el token. En el proceso tenemos que crear una cuenta (con datos cualesquiera, pero obviamente nick SQLazo :P ) y tras el último link, podemos ver la flag. La razón es la previamente dicha: **No invalidan el token de OAUTH tras el primer uso**.

<p align="center">
  <img src="imgs/web/fintechno_solution.PNG">
</p>

**bitup20{R3us34uth0r1z4t10nT0k3nsIs4b4dId34}**


## Web - Curvas Peligrosas

<p align="center">
  <img src="imgs/web/curvas_peligrosas.png">
</p>

Entramos a la web y vemos que piden hacer un login. Si no somos *admin*, dice que no podemos ver la flag, pero al tratar entrar como *admin*, sale un mensaje de error por no estar autorizados. Estudiamos la petición HTTP en el navegador y encontramos una **cookie** con un **JWT**. Lo abrimos [aquí](https://jwt.io/) y vemos que uno de los campos de la cabecera es `jku` con la url donde está su clave pública para verificar la firma. Vemos ahí y también en el JWT que es un cifrado [ES256](https://ldapwiki.com/wiki/ES256). 

Para resolver el reto tuvimos que cambiar el token por uno con `"usuario" : "admin"` y que esa url a que apunte a nuestro servidor local. Ahí tendremos un fichero `jwks.json` con la clave pública que verifica la privada con la que firmaremos nuestro nuevo JWT. Yo en el proceso tuve algún problema con las claves de ES256 así que decidí generar una clave RS256 y hacer el mismo proceso cambiando el campo `alg` del JWT. De todos modos, se podía hacer con ES256 sin cambiar esto.

Para generar claves tanto ES256 como RS256 (y otros más) se puede usar [este sitio](https://mkjwk.org/). Luego editando en jwt.io el token anterior que teníamos y firmando con nuestras nuevas claves, obtenemos esto:

<p align="center">
  <img src="imgs/web/curves1.PNG">
</p>

Esta es la clave que tenía en mi servidor local corriendo con ese comando que sale en pantalla:

<p align="center">
  <img src="imgs/web/curves2.PNG">
</p>

Ahora simplemente cambiando la cookie de la petición (se puede usar un proxy inverso como Burp, o simplemente *Editar y volver a enviar* desde Firefox) y reenviándola, podremos ver la flag.

<p align="center">
  <img src="imgs/web/curves_solution.PNG">
</p>

**bitup20{mas_peligrosas_que_la_cruz_verde}**


## Atomics - Hello World

<p align="center">
  <img src="imgs/atomics/hello_world.png">
</p>

Un **base64** muy evidente. <a href="https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true)&input=WW1sMGRYQXlNSHQxYmpSZmJuVXpkalJmTTJReFkyTXhNRzVmTUc1c01XNHpmUT09IA">Aquí</a> está la solución:

**bitup20{un4_nu3v4_3d1cc10n_0nl1n3}**


## Atomics - Demiguise

<p align="center">
  <img src="imgs/atomics/demiguise.png">
</p>

Era otro reto muy sencillo. Siguiendo la idea de la descrìpción, se podía encontrar la flag en el *código fuente* (no hice captura al resolverlo así que tomo la imagen del writeup de los creadores):

<p align="center">
  <img src="imgs/atomics/demiguise_solution.jpg">
</p>

**bitup20{lo_esencial_es_invisible_para_los_ojos}**


## Atomics - Hexa

<p align="center">
  <img src="imgs/atomics/hexa.png">
</p>

El tercero de los retos simples de Atomics. Nos dicen que es un cifrado en **hexadecimal** así que lo resolvemos una vez más con <a href="https://gchq.github.io/CyberChef/#recipe=From_Hex('Space')&input=NjIgNjkgNzQgNzUgNzAgMzIgMzAgN2IgNmMgMzAgNWYgNzMgMzQgNjIgMzMgNmUgN2Q">CyberChef</a>.

**bitup20{l0_s4b3n}**


## Atomics - Helius 5

Ficheros: <a href="challs/message.wav">message.wav</a>

<p align="center">
  <img src="imgs/atomics/helius_5.png">
</p>

Bueno, este reto presenta una bonita historia y nos da un archivo de audio. Lo reproducimos y parece **código morse**, lo cual concuerda con la historia de la descripción. Vamos a decodificarlo en [este sitio](https://morsecode.world/international/decoder/audio-decoder-adaptive.html) por comodidad:

<p align="center">
  <img src="imgs/atomics/helius5_solution.PNG">
</p>

**bitup20{CTHULHU}** (al parecer también valían *Cthulhu* y *cthulhu*)


## Atomics - Un Ciudadano Ejemplar

Ficheros: <a href="challs/me.zip">me.zip</a>

<p align="center">
  <img src="imgs/atomics/un_ciudadano_ejemplar.png">
</p>

Nos dan un fichero comprimido que tras comprobar con los típicos comandos `file me.zip`, `7z l me.zip` y `zipnote me.zip`, que no hay nada raro, tratamos de descomprimirlo.

Ahí vemos que los ficheros están protegidos con contraseña, así que tendremos que crackear el zip. Como en la descripción hablan del *rock*, mi primera idea fue buscar un wordlist de canciones de rock, pero luego resultó ser mucho más sencillo y era una referencia a **rockyou.txt**, el típico wordlist de Kali. De todos modos probando con el wordlist por defecto de **john** es capaz de extraer la simple contraseña **rabbit**. Antes de poder crackearlo hay que usar **zip2john** para extraer los hashes.

<p align="center">
  <img src="imgs/atomics/ciudadano1.PNG">
</p>

Una vez la tenemos, ya descomprimimos y en el fichero *flag.txt* tenemos la flag:

<p align="center">
  <img src="imgs/atomics/ciudadano_solution.PNG">
</p>

**bitup20{nunca_te_fies_de_las_apariencias}**
