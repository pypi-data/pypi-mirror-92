import getpass
_userName = getpass.getuser()

import subprocess
import sys
def pip_install(package):
    subprocess.check_call(["pip", "install", package])

try:
    _data = open(f'C:\\Users\\{_userName}\\Documents\\python3_vsave.txt', 'r+')
except:
    open(f'C:\\Users\\{_userName}\\Documents\\python3_vsave.txt', 'w').close()
    _data = open(f'C:\\Users\\{_userName}\\Documents\\python3_vsave.txt', 'r+')
_dataList = _data.readlines()

def upload(name, value):
    global _data
    global _dataList
    if str(type(value)) == "<class 'str'>":
        _data.write(f"{name} = '{str(value)}'\n")
    else:
        _data.write(f"{name} = {value}\n")

def download(name):
    global _data
    global _dataList
    _data = open(f'C:\\Users\\{_userName}\\Documents\\python3_vsave.txt', 'r+')
    _Data = list(reversed(list(_data)))
    for i in _Data:
        if i[0:len(name)] == name:
            _value = i
            _value.replace('\n', '')
            break
    else:
        raise NameError("Variable name '%s' is not defined" % (name))
    return _value