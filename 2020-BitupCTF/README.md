# Write-up BitupCTF

* [Misc - Inosmnia](#misc---insomnia)
* [Web - Fintechno](#web---fintechno)
* [Web - Curvas Peligrosas](#web---curvas-peligrosas)
* [Atomics - Hello World](#atomics---hello-world)
* [Atomics - Demiguise](#atomics---demiguise)
* [Atomics - Hexa](#atomics---helius5)
* [Atomics - Helius 5](#atomics---hexa)
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
* 3 últimas líneas de código en un bloque if...else 

El problema de todo esto es que el código parece estar bastante ofuscado, teniendo las variables y funciones nombres muy extraños. Toca entonces renombrarlos con Sublime para tratar de comprender qué hace el código. 
Tras el proceso de *beautify* del script y dándome cuenta de que uno de los valores hardcodeados es *RightToLeft* cifrado (simplemente permite entender mejor que esa función lo que hace es invertir los caracteres), [este es el script resultante](./challs/clean.ps1).

<p align="center">
  <img src="imgs/misc/insomnia2.PNG">
</p>


 
<p align="center">
  <img src="imgs/misc/insomnia_solution.PNG">
</p>

**FLAG{ECB_IS_NOT_SECURE}**

