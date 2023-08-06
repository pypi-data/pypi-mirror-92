# -*- coding: utf-8 -*-
"""HostHome-CLI ara login y empezara tu cli
Usage:
  hosthome empezar               [-v | --verbose]
  hosthome eliminar              [-v | --verbose]
Opciones:
  -h --help                      Muestra esta pantalla.
  -v --version                   Show version.
"""

from docopt import docopt
import platform
from termcolor import cprint
from warnings import warn
import sys, os, requests

from hosthome.version import VERSION as __version__
from hosthome.login import login

url = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]
docs = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["docs"]

verbose = False

def mirarSiUsuarioEsImbecil(s: str, i: bool = False):
  if s == "":
    cprint("Pon un argumento valido", "red")
    sys.exit(1)
  if i:
    if s not in "ruby,python,nodejs,scala,clojure,cs,php".split(","):
      cprint("Pon un argumento valido", "red")
      sys.exit(1)          

archivo = """
run = "tempCmdStart"
len = "tempLen"

----- ADVERTENCIA
NO MENTIR SOBRE LA INFORMACION SINO EL HOST SERA ELIMINADO
NO TOCAR NADA A NO SER QUE SEA NECESARIO

SI OCURRE UN ERROR PODEIS PONERLO AQUI (https://github.com/HostHome-of/python-CLI/issues)
-----
"""

def crearArchivo(Lenguage: str, cmd: str):
  if verbose:
    print("\n ---- Logs")
    print("Creando archivo...")
  try:
    data = open(".host.home", "x")
  except:
    if verbose:
      print("Archivo localizado")
      print("Eliminando archivo...")
    os.remove(".host.home")
    if verbose:
      print("Recreando...")
    data = open(".host.home", "x")
  if verbose:
    print("Escribiendo archivo...")
  archivo2 = str(archivo
                .replace("tempLen", Lenguage)
                .replace("tempCmdStart", cmd)
                )
  data.write(archivo2)
  cprint("¡ya esta!")

def main():

  try:
    args = docopt(__doc__, version="HostHome-CLI | version :: {}".format(__version__))

    if platform.system() != "Windows":
      warn("Encontré un sistema que no es Windows. Es posible que la instalación del paquete no funcione.")

    if args["empezar"]:    

      data = login()
      cprint(f"\nBienvenido {data['nombre']}\n", "green")
      instalacion = input("Pon el comando para ejecutar el programa :: ")
      mirarSiUsuarioEsImbecil(instalacion)
      lenguage = input(f"Pon el idioma en el que esta \n * ruby\n * python\n * nodejs\n * scala\n * clojure\n * cs\n * php\n MIRAR DOCS URGENTE ({docs}) :: ").strip()
      mirarSiUsuarioEsImbecil(lenguage, i=True)

      if "--verbose" in args:
        verbose = True

      crearArchivo(lenguage, instalacion)

      sys.exit(0)
  except Exception as e:
    print(e)