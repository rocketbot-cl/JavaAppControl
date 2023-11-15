# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

"""
    Obtengo el modulo que fue invocado
"""

import os
import sys
import traceback

base_path = tmp_global_obj["basepath"]
cur_path = os.path.join(base_path, 'modules', 'JavaAppControl', 'libs')

cur_path_x64 = os.path.join(cur_path, 'Windows' + os.sep +  'x64' + os.sep)
cur_path_x86 = os.path.join(cur_path, 'Windows' + os.sep +  'x86' + os.sep)

if sys.maxsize > 2**32 and cur_path_x64 not in sys.path:
    sys.path.append(cur_path_x64)
elif sys.maxsize < 2**32 and cur_path_x86 not in sys.path:
    sys.path.append(cur_path_x86)

import TkinterForm
import JABHandle
import PlayerController
import json
from ctypes import *
from ctypes import wintypes


module = GetParams("module")
global root
global hwnd_app
global root_app

if module == "JavaScope":
    try:
        print("\t \t ***JavaScope*** \n")
        root = TkinterForm.tk.Tk()
        root.withdraw()
        app = TkinterForm.Application(master=root)
        app.run_dll()
        root.after(3000, lambda: root.destroy()) # Destroy the widget after 1 seconds
        app.mainloop()
        selector = GetParams("Selector")
        result = GetParams("result")
        res = json.loads(selector.replace("'", '"'))
        title = res['title']
        
        hwnd_app = JABHandle.get_hwnd_by_title(title)
        print(hwnd_app)
        print(title)
        if hwnd_app:
            app_java = JABHandle.get_app_java_by_hwnd(hwnd_app)
            print(app_java)
            current_context = JABHandle.AccessibleContextInfo()
            root_app = JABHandle.getACInfo(app_java['vm_id'], app_java['ac'], current_context, None)
            SetVar(result, True)
        else:
            SetVar(result, False)
    except Exception as e:
        SetVar(result, False)
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e

if module == "setClick":
    try:
        print("\t \t ***Click*** \n")
        selector = GetParams("Selector")
        res = json.loads(selector)
        indices = res['indices']
        app_java = JABHandle.get_app_java_by_hwnd(hwnd_app)
        componente = JABHandle.search_children(app_java, indices)
        try:
            if componente != False:
                bounds_component = {'x': componente.x, 'y': componente.y, 'width': componente.width, 'heigth': componente.height }
                PlayerController.do_click(bounds_component)
            else:
                children = JABHandle.search_by_index(root_app, indices)
                componente1 = JABHandle.AccessibleContextInfo()
                JABHandle.bridgeDll.getAccessibleContextInfo(children.vm_id ,children.ac_ptr ,byref(componente1))
                bounds_component = {'x': componente1.x, 'y': componente1.y, 'width': componente1.width, 'heigth': componente1.height }
                #bounds_component = {'x': children.ac_info.x, 'y': children.ac_info.y, 'width': children.ac_info.width, 'heigth': children.ac_info.height }
                PlayerController.do_click(bounds_component)
        except:
            componente_tercera_busqueda = JABHandle.search_component_in_list(res)
            bounds_component = {'x': componente.x, 'y': componente.y, 'width': componente.width, 'heigth': componente.height }
            PlayerController.do_click(bounds_component)
    except Exception as e:
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e

if module == "getTextEvent":
    try:
        selector = GetParams("Selector")
        result = GetParams("result")
        res = json.loads(selector)
        indices = res['indices']
        app_java = JABHandle.get_app_java_by_hwnd(hwnd_app)
        componente, textItemsInfo = JABHandle.search_children(app_java, indices, True)
        try:
            if componente != False:
                texto = textItemsInfo.sentence
                if len(texto) <= 0:
                    texto = componente.name
                print("Este es el texto: " + str(texto))
                SetVar(result, texto)
        except:
            componente_tercera_busqueda = JABHandle.search_component_in_list(res)
            texto = componente_tercera_busqueda.name
            print("Este es el texto: " + str(texto))
            SetVar(result, texto)
    except Exception as e:
        traceback.print_exc()
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e

if module == "setText":
    try:
        print("\t \t ***SetText*** \n")
        selector = GetParams("Selector")
        text = GetParams("Text")
        res = json.loads(selector)
        indices = res['indices']
        app_java = JABHandle.get_app_java_by_hwnd(hwnd_app)
        componente = JABHandle.search_children(app_java, indices)
        try:
            if componente != False:
                bounds_component = {'x': componente.x, 'y': componente.y, 'width': componente.width, 'heigth': componente.height }
                PlayerController.do_click(bounds_component)
                PlayerController.set_text(bounds_component, text)
            else:
                print("Else!")
                children = JABHandle.search_by_index(root_app, indices)
                componente1 = JABHandle.AccessibleContextInfo()
                JABHandle.bridgeDll.getAccessibleContextInfo(children.vm_id ,children.ac_ptr ,byref(componente1))
                bounds_component = {'x': componente1.x, 'y': componente1.y, 'width': componente1.width, 'heigth': componente1.height }
                PlayerController.do_click(bounds_component)
                bounds_component = {'x': componente1.x, 'y': componente1.y, 'width': componente1.width, 'heigth': componente1.height }
                PlayerController.set_text(bounds_component, text)
        except:
            componente_tercera_busqueda = JABHandle.search_component_in_list(res)
            bounds_component = {'x': componente.x, 'y': componente.y, 'width': componente.width, 'heigth': componente.height }
            PlayerController.do_click(bounds_component)
            PlayerController.set_text(bounds_component, text)
    except Exception as e:
        print("\x1B[" + "31;40mAn error occurred\u2193\x1B[" + "0m")
        PrintException()
        raise e
    


