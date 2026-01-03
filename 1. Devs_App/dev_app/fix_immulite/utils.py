import winreg

def save_registry_int(variable: int(),variable_name = "variable_int",path="Software\\IMMUNLITE"):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path , 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
    winreg.SetValueEx(key, variable_name, 0, winreg.REG_DWORD, variable)
    winreg.CloseKey(key)

def save_registry_string(variable: str(),variable_name = "variable_string",path="Software\\IMMUNLITE"):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
    winreg.SetValueEx(key, variable_name, 0, winreg.REG_SZ, variable)
    winreg.CloseKey(key)

def load_registry(name_var:str(),path="Software\\IMMUNLITE"):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        variable, _ = winreg.QueryValueEx(key, name_var)
        winreg.CloseKey(key)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
        winreg.SetValueEx(key, name_var, 0, winreg.REG_DWORD, 0)
        variable = 0
    return variable