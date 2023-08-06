import requests
from getpass import getpass
from termcolor import cprint

import webbrowser, requests

url = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]

def login():
    
    print("\t\t\t\t\t"+"-"*33)
    print("\t\t\t\t\t"+"|\t"+"                 \t|")
    print("\t\t\t\t\t"+"|\t"+"Login en HostHome\t|")
    print("\t\t\t\t\t"+"|\t"+"                 \t|")
    print("\t\t\t\t\t"+"-"*33)

    mail = input("Porfavor escribe tu email :: ")
    psw = getpass("Escribe tu contraseña :: ")
    
    data = requests.post(f"{url}login?psw={psw}=&mail={mail}").json()

    if data == {}:
        cprint("Esa cuenta no existe intentalo otra vez", "red")
        si_no = input("\n¿Quieres crearte una? [s/n] :: ")
        if si_no == "s":
            webbrowser.open(f'{url}register', new=2)
            return login()
        else:
            cprint("Veo que no", "red")
            exit(0)

    return data
