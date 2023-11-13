



# JavaAppControl
  
Module for clicking, writing and extracting text from Java applications  

*Read this in other languages: [English](Manual_JavaAppControl.md), [Português](Manual_JavaAppControl.pr.md), [Español](Manual_JavaAppControl.es.md)*
  
![banner](imgs/Banner_JavaAppControl.png)
## How to install this module
  
To install the module in Rocketbot Studio, it can be done in two ways:
1. Manual: __Download__ the .zip file and unzip it in the modules folder. The folder name must be the same as the module and inside it must have the following files and folders: \__init__.py, package.json, docs, example and libs. If you have the application open, refresh your browser to be able to use the new module.
2. Automatic: When entering Rocketbot Studio on the right margin you will find the **Addons** section, select **Install Mods**, search for the desired module and press install.  


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
