from ctypes import *
import comtypes.client
import win32com.client
from ctypes import wintypes
import win32gui
import win32con
import os
from time import sleep
import PlayerController

jchar = c_wchar
jint = c_int
jfloat = c_float
jboolean = c_bool

bridgeDll = None
bridgeEnabled = False
MAX_STRING_SIZE = 1024
SHORT_STRING_SIZE = 256
handleInfo = []
lista_comp = []

def enableBridge():
	global A11Y_PROPS_CONTENT
	global bridgeEnabled
	A11Y_PROPS_CONTENT = (
		"assistive_technologies=com.sun.java.accessibility.AccessBridge\nscreen_magnifier_present=true\n"
	)
	with open(os.path.expanduser(r"~\.accessibility.properties"), "wt") as props:
		props.write(A11Y_PROPS_CONTENT)

	bridgeEnabled = True


def initializeAccessBridge():
	global bridgeDll
	global bridgeEnabled
	try:
		if bridgeEnabled == False:
			enableBridge()
			load_library()
		
			while (bridgeDll.Windows_run() != 1):
				print("Estado de Access Bridge: " + str(bridgeDll.Windows_run()))
				sleep(1)
		
			_fixBridgeFuncs()
			print("Se cargo la DLL correctamente!")
	except:
		print("Error al cargar la dll WindowsAccessBridge")


def load_library():
	global bridgeDll
	dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
	print("DIRECTORY PATH: ", dir_path)
	try:
		bridgeDll = cdll.LoadLibrary(dir_path + 'WindowsAccessBridge-32')
	except:
		try:
			bridgeDll = cdll.LoadLibrary(dir_path + 'WindowsAccessBridge-64')
		except Exception as e:
			print(e)

def GetCursorPos():
    """
    GetCursorPos from Win32.
    Get current mouse cursor positon.
    Return Tuple[int, int], two ints tuple (x, y).
    """
    point = wintypes.POINT(0, 0)
    windll.user32.GetCursorPos(byref(point))
    return point.x, point.y


def getHandle(filter_):
    
	handleInfo = []
	#print(handleInfo)

	def winEnumHandler(hwnd, ctx):
		nonlocal handleInfo
		if win32gui.IsWindowVisible(hwnd):
			handleInfo.append((hwnd, win32gui.GetWindowText(hwnd)))

	win32gui.EnumWindows(winEnumHandler, None)
	
	handle = [handle for handle in handleInfo if handle[1] == filter_][0]
	print(handle)
	return handle[0]

def explorer(hwnd):
	global bridgeDll
	initializeAccessBridge()
	vmID = vmid2 = c_long()
	ac = accContext = c_int64()
	try:
		if (bridgeDll.isJavaWindow(hwnd) == 1):
			print("Es una ventana Java!")
			bridgeDll.getAccessibleContextFromHWND(
				hwnd, byref(vmID), byref(accContext))
			#print("vmID: " + str(vmID) + "\n accContext: " + str(accContext))
			print("ID Maquina Virtual de Java: " + str(vmID))
			print("Esperando 3 segundos...")
			sleep(3)
			x, y = GetCursorPos()
			print("X: " + str(x) + ", Y: " + str(y))
			bridgeDll.getAccessibleContextAt(vmID, accContext, x, y, byref(ac))
			#print("Ac: " + str(ac))
			accessibleContextInfo = AccessibleContextInfo()
			bridgeDll.getAccessibleContextInfo(
				vmID, accContext, byref(accessibleContextInfo))
			print("Nombre del componente: " + str(accessibleContextInfo.name))
			print("Nombre del role: " + str(accessibleContextInfo.role))
			selector = get_selector(vmID, ac, hwnd)
			print("Selector: " + str(selector))
	except:
		print("Excepcion")

def get_selector(vmID, ac, hwnd):
	index_selector = []
	title_app = ""
	component = AccessibleContextInfo()
	bridgeDll.getAccessibleContextInfo(vmID,ac,byref(component))
	while ac.value != 0:
		accessibleContextInfo  = AccessibleContextInfo()
		bridgeDll.getAccessibleContextInfo(vmID,ac,byref(accessibleContextInfo))
		if accessibleContextInfo.indexInParent != -1:
			index_selector.append(accessibleContextInfo.indexInParent)
		if bridgeDll.getAccessibleParentFromContext(vmID, ac) == 0:
			title_app = accessibleContextInfo.name
		ac_aux = bridgeDll.getAccessibleParentFromContext(vmID, ac)
		ac_aux = c_int64(ac_aux)
		bridgeDll.releaseJavaObject(vmID, ac)
		ac = ac_aux
	selector = {
		'title' : title_app, 'indices' : index_selector, 'component' : {
			'name' : component.name,
			'role' : component.role,
			'index' : component.indexInParent
		}
	}
	componente = find_component(selector)
	bounds_component = {'x': componente.x, 'y': componente.y, 'width': componente.width, 'heigth': componente.height }
	#PlayerController.do_click(bounds_component)
	#print("Por setear texto")
	#PlayerController.set_text(bounds_component, "Hola! Aguante rocketbot")
	return selector

def winEnumHandler(hwnd, ctx):
	global handleInfo
	if win32gui.IsWindowVisible(hwnd):
		handleInfo.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_list_hwnd_java_apps():
	java_hwnd_apps = []
	win32gui.EnumWindows(winEnumHandler, None)
	for hwnd in handleInfo:
		#print(hwnd)
		if bridgeDll.isJavaWindow(hwnd[0]) == 1:
			java_hwnd_apps.append(hwnd[0])
	return java_hwnd_apps

def get_hwnd_by_title(title):
	global handleInfo
	handleInfo = []
	win32gui.EnumWindows(winEnumHandler, None)
	print("Listado ",handleInfo)
	for hwnd in handleInfo:
		#print(hwnd)
		if hwnd[1] == title:
			return hwnd
	return ""

def get_app_java_by_hwnd(hwnd, not_maximize = False):
    
	print("WINDOW: ", bridgeDll.isJavaWindow(hwnd[0]))
	
	if bridgeDll.isJavaWindow(hwnd[0]) == 1:
		try:
			if not_maximize:
				win32gui.ShowWindow(hwnd[0], win32con.SW_SHOWNORMAL)
			else:
				win32gui.ShowWindow(hwnd[0], win32con.SW_SHOWMAXIMIZED)
			shell = win32com.client.Dispatch("WScript.Shell")
			shell.SendKeys('%')
			win32gui.SetForegroundWindow(hwnd[0])
		except:
			print("No se pudo maximizar la ventana")
		vm_id = c_long()
		ac = c_int64()
		bridgeDll.getAccessibleContextFromHWND(hwnd[0], byref(vm_id), byref(ac))
		app_info = {'title' : hwnd[1], 'ac' : ac, 'vm_id': vm_id}
		return app_info

def get_list_java_apps(java_hwnd_apps):
	java_apps = []
	for hwnd in java_hwnd_apps:
		vm_id = c_long()
		ac = c_int64()
		bridgeDll.getAccessibleContextFromHWND(hwnd, byref(vm_id), byref(ac))
		app_java = AccessibleContextInfo()
		bridgeDll.getAccessibleContextInfo(vm_id, ac, byref(app_java))
		app_info = {'title': app_java.name,
					'ac': ac, 'vm_id': vm_id, 'hwnd': hwnd}
		java_apps.append(app_info)
	return java_apps


def get_app_java(title, java_apps):
	for app in java_apps:
		if app['title'] == title:
			return app
		else:
			bridgeDll.releaseJavaObject(app['vm_id'], app['ac'])

def find_component(component):
	java_hwnd_apps = get_list_hwnd_java_apps()
	java_apps = get_list_java_apps(java_hwnd_apps)
	title = component['title']
	app = get_app_java(title, java_apps)
	indices = component['indices']
	foundComponent = search_children(app, indices)
	return foundComponent

def search_children(app, indices, getText = False):
	initializeAccessBridge()
	ac = app['ac']
	vm_id = app['vm_id']
	indices.reverse()
	try:
		for index in indices:
			child_info = AccessibleContextInfo()
			bridgeDll.getAccessibleContextInfo(vm_id, ac, byref(child_info))
			child = bridgeDll.getAccessibleChildFromContext(vm_id, ac, index)
			child = c_int64(child)
			bridgeDll.releaseJavaObject(vm_id, ac)
			ac = child
		child_info = AccessibleContextInfo()
		bridgeDll.getAccessibleContextInfo(vm_id, ac, byref(child_info))
		textItemsInfo=AccessibleTextItemsInfo()
		bridgeDll.getAccessibleTextItems(vm_id, ac, byref(textItemsInfo), 0)
		bridgeDll.releaseJavaObject(vm_id, ac)
		bridgeDll.releaseJavaObject(vm_id, child)
		if getText == True:
			return child_info,textItemsInfo
		else:
			return child_info
	except:
		import traceback
		traceback.print_exc()
		print("Error al encontrar el elemento")
		return False


def get_text(vm_id, new_ac):
	textItemsInfo=AccessibleTextItemsInfo()
	bridgeDll.getAccessibleTextItems(vm_id,new_ac,byref(textItemsInfo),0)
	return textItemsInfo.word


def getACInfo(vm_id, current_ptr, current_context, parent_item):
	global lista_comp
	if bridgeDll.getAccessibleContextInfo(vm_id, current_ptr, byref(current_context)):
		newItem = build_accesible_tree(
			current_context, vm_id, current_ptr, parent_item)
		newItem.parent = parent_item
		for index in range(0, current_context.childrenCount):
			if current_context.role_en_US != "unknown" and "visible" in current_context.states_en_US:
				child_context = AccessibleContextInfo()
				ac_child_ptr = bridgeDll.getAccessibleChildFromContext(
					vm_id, current_ptr, index)
				ac_child = c_int64(ac_child_ptr)
				getACInfo(vm_id, ac_child, child_context, newItem)
		return newItem
	else:
		current_context = AccessibleContextInfo()


def build_accesible_tree(ac_info, vm_id, ac_ptr, parent_item):
	if ac_info != None:
		item = JABObject(ac_info, vm_id, ac_ptr)
		if parent_item != None:
			parent_item.children.append(item)
		global lista_comp
		lista_comp.append(item)
		return item
	return None

def search_by_index(root, indices):
	for index in indices:
		root = root.children[index]
	return root

def search_component_in_list(componente):
	#{"title":"Calculator PH","component":{"index":1,"name":"2","role":"push button"},"indices":[1,2,0,0,0,0]}
	global lista_comp
	for comp in lista_comp:
		comp = comp.ac_info
		if (componente["component"]["index"] == comp.indexInParent) and (componente["component"]["name"] == comp.name) and (componente["component"]["role"] == comp.role): 
			return comp
	return None


def _errcheck(res, func, args):
	if not res:
		raise RuntimeError("Result %s" % res)
	return res


def _fixBridgeFunc(restype, name, *argtypes, **kwargs):
	try:
		func = getattr(bridgeDll, name)
	except AttributeError:
		print("%s not found in Java Access Bridge dll" % name)
		return
	func.restype = restype
	func.argtypes = argtypes
	if kwargs.get('errcheck'):
		func.errcheck = _errcheck


def _fixBridgeFuncs():
	"""Appropriately set the return and argument types of all the access bridge dll functions
	"""
	_fixBridgeFunc(c_int64, 'getAccessibleParentFromContext', c_long, c_int64)
	_fixBridgeFunc(c_int64, 'getAccessibleChildFromContext',
				   c_long, c_int64, jint, errcheck=True)
	_fixBridgeFunc(c_bool, 'getAccessibleTextItems', c_long, c_int64,
				   POINTER(AccessibleTextItemsInfo), jint, _errcheck=True)

#Definitions of access bridge types, structs and prototypes

class AccessibleContextInfo(Structure):
    	_fields_ = [
        ('name', wintypes.WCHAR * MAX_STRING_SIZE),
        ('description', wintypes.WCHAR * MAX_STRING_SIZE),
        ('role', wintypes.WCHAR * SHORT_STRING_SIZE),
        ('role_en_US', wintypes.WCHAR * SHORT_STRING_SIZE),
        ('states', wintypes.WCHAR * SHORT_STRING_SIZE),
        ('states_en_US', wintypes.WCHAR * SHORT_STRING_SIZE),
        ('indexInParent', jint),
        ('childrenCount', jint),
        ('x', jint),
        ('y', jint),
        ('width', jint),
        ('height', jint),
        ('accessibleComponent', wintypes.BOOL),
        ('accessibleAction', wintypes.BOOL),
        ('accessibleSelection', wintypes.BOOL),
        ('accessibleText', wintypes.BOOL),
        ('accessibleValue', wintypes.BOOL),
	]


class AccessibleTextItemsInfo(Structure):
	_fields_ = [
        ('letter', wintypes.WCHAR),
        ('word', wintypes.WCHAR * SHORT_STRING_SIZE),
        ('sentence', wintypes.WCHAR * MAX_STRING_SIZE),
	]


class JABObject():
	def __init__(self, data, vm_id, ac_ptr):
		self.ac_info = AccessibleContextInfo()
		self.ac_info = data
		self.children = []
		self.vm_id = vm_id
		self.ac_ptr = ac_ptr
		self.parent = None