# JavaApp Control
  
Modulo para automatizar aplicaciones Java  

*Read this in other languages: [English](Manual_JavaAppControl.md), [Español](Manual_JavaAppControl.es.md).*
  
![banner](imgs/Banner_JavaAppControl.png)
## Como instalar este módulo
  
__Descarga__ e __instala__ el contenido en la carpeta 'modules' en la ruta de Rocketbot.  



## Descripción de los comandos

### Conectar ventana
  
Conectar una ventana
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Selector|Selector de ventana Java|{ title: 'Titulo ventana' }|
|Resutlado|Variable donde se almacena el resultado sin {}|{resultado}|

### Click
  
Hace un click en un componente Java
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Selector|Propiedad de texto utilizada para encontrar un elemento de IU particular cuando se ejecuta la actividad.|...|

### Obtener Texto
  
Extrae un valor de texto de un elemento de IU Java especificado.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Selector|Propiedad de texto utilizada para encontrar un elemento de IU Java particular cuando se ejecuta la actividad. |...|
|Resultado|Variable donde se almacena el resultado sin {}|{resultado}|

### Set Text
  
Le permite escribir una cadena en el atributo texto de un elemento de IU Java especificado.
|Parámetros|Descripción|ejemplo|
| --- | --- | --- |
|Selector|Propiedad de texto utilizada para encontrar un elemento de IU Java particular cuando se ejecuta la actividad.|...|
|Texto|Texto o variable que se vá a escribir en el atributo text del objeto Java.|Texto|
