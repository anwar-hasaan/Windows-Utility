import winreg
import os, time
from getpass import getuser


class StartupRegistry:
    """
    Dependencies:
    import os
    import winreg
    from getpass import getuser
    Caution: This class work only on windows machine
    """
    def __init__(self) -> None:
        self.APP_PATH = None #Set APP_Path to this after calling is_in_registry if True
        self.STARTUP_COPY_DIR = r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\"Start Menu"\Programs\Startup'.format(getuser())

    def set_startup_config(self) -> bool:
        """
        It will copy it self to the startup dir
        and add the it self path to the registry
        only this function is enough to set a itself to run at startup
        """
        file_path = os.path.realpath(__file__)
        basename = os.path.basename(file_path)
        STARTUP_PATH = os.path.join(self.STARTUP_COPY_DIR.replace('"', ''), basename)
        
        if file_path != STARTUP_PATH:
            try:
                os.system("copy {} {}".format(file_path, self.STARTUP_COPY_DIR)) #copy this file to STARTUP_DIR
                print('file copied')
                return True
            except:
                pass
            try:
                filename = basename.split('.')[0]
                self.set_startup_registry(filename, STARTUP_PATH)
                print('seted to the registry')
                return True
            except: pass
        return False
        

    def is_in_startup_registry(self, app_name:str) -> bool:
        """
        Param: take possible registry app_name 
        Return: True if app_name exists is startup registry else return False
        """
        with winreg.OpenKey(key=winreg.HKEY_CURRENT_USER, sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run',
        reserved=0, access=winreg.KEY_ALL_ACCESS) as key:
            index = 0
            while index <= 100:     # Max 1.000 values
                try:
                    key_name, key_value, _ = winreg.EnumValue(key, index)
                    if (key_name == app_name) or (key_name == app_name+'_py'):
                        self.APP_PATH = key_value
                        return True
                    index += 1
                except:
                    break
            return False
    
    def set_startup_registry(self, app_name, app_path=None, auto_start=True) -> bool:
        """"
        Param: take app_name as restry key name and app_path as
        registry key value auto_start as startup=True
        Return: If the function fails, OSError is raised else return True
        """
        with winreg.OpenKey(key=winreg.HKEY_CURRENT_USER, sub_key=r'Software\Microsoft\Windows\CurrentVersion\Run', 
                        reserved=0, access=winreg.KEY_ALL_ACCESS) as key:
            try:
                if auto_start:
                    if self.is_in_startup_registry(app_name):
                        if self.APP_PATH == app_path:
                            return True
                        app_name = str(app_name) + '_py'
                    winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, app_path)
                else:
                    if self.is_in_startup_registry(app_name):
                        winreg.DeleteValue(key, app_name)
                    if self.is_in_startup_registry(app_name+'_py'):
                        winreg.DeleteValue(key, app_name+'_py')
            except OSError:
                return False
        return True


#Example useages
reg = StartupRegistry()
reg.set_startup_config()
