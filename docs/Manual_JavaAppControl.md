# JavaApp Control
  
Modulo para automatizar aplicaciones Java  

*Read this in other languages: [English](Manual_JavaAppControl.md), [Español](Manual_JavaAppControl.es.md).*
  
![banner](imgs/Banner_JavaAppControl.png)
## How to install this module
  
__Download__ and __install__ the content in 'modules' folder in Rocketbot path  



## Description of the commands

### Connect window
  
Connect a window
|Parameters|Description|example|
| --- | --- | --- |
|Selector|Java window selector|{ title: 'Window title' }|
|Result|Variable where the result is stored without {}|{result}|

### Click
  
Do a click in a Java component
|Parameters|Description|example|
| --- | --- | --- |
|Selector|Text property used to find a particular UI element when the activity is executed.|...|

### Get Text
  
Extracts a text value from a specified UI Java element.
|Parameters|Description|example|
| --- | --- | --- |
|Selector|Text property used to find a particular UI element when the activity is executed.|...|
|Result|Variable where the result is stored without {}|{result}|

### Set Text
  
Enables you to write a string to the text attribute of a specified UI Java element.
|Parameters|Description|example|
| --- | --- | --- |
|Selector|Text property used to find a particular UI Java element when the activity is executed.|...|
|Text|The string or variable that is to be written to the text attribute of a UI Java element.|Text|
