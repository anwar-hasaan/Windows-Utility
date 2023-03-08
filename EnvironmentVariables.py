import winreg

class Win32Environment:
    """
    Utility class to get/set/delete windows environment variable
    """
    def __init__(self, scope):
        assert scope in ('user', 'system')
        self.scope = scope
        if scope == 'user':
            self.root = winreg.HKEY_CURRENT_USER
            self.subkey = 'Environment'
        else:
            self.root = winreg.HKEY_LOCAL_MACHINE
            self.subkey = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
            
    def getenv(self, name):
        try:
            key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(key, name)
            winreg.CloseKey(key)
            return value
        except: return ''
    
    def setenv(self, name, value):
        try:
            # Note: for 'system' scope, you must run this as Administrator
            key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
            winreg.CloseKey(key)
            return True
        except: return False
    
    def remove(self, name):
        try:
            key = winreg.OpenKey(self.root, self.subkey, 0, winreg.KEY_ALL_ACCESS)
            winreg.DeleteValue(key, name)
            return True
        except: return False

env_name = 'SENT'
env_value = 'False'
env = Win32Environment('user') #user scope

value = env.getenv(env_name) #return string
if not value or (value != env_value):
    env.setenv(env_name, env_value) #return true/false

#to delete an existsing key value
# env.remove(env_name)