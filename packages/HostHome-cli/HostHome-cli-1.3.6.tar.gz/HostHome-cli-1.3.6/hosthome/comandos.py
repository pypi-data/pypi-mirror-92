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
  try:
    data = open(".host.home", "x")
  except:
    os.remove(".host.home")
    data = open(".host.home", "x")
  archivo2 = str(archivo
                .replace("tempLen", main)
                .replace("tempCmdStart", cmd)
                )
  data.write(archivo2)

def main():

  try:
    args = docopt(__doc__, version="HostHome-CLI | version :: {}".format(__version__))

    if platform.system() != "Windows":
      warn("Encontré un sistema que no es Windows. Es posible que la instalación del paquete no funcione.")

    if args["empezar"]:    

      data = login()
      cprint(f"> Hola {data['nombre']}", "green")
      instalacion = input("Pon el comando para comenzar la instalacion :: Ej: npm i ")
      mirarSiUsuarioEsImbecil(instalacion)
      lenguage = input(f"Pon el idioma en el que esta \n * ruby\n * python\n * nodejs\n * scala\n * clojure\n * cs\n * php\n MIRAR DOCS URGENTE ({url}docs) :: ").strip()
      mirarSiUsuarioEsImbecil(lenguage, i=True)

      if args["-v"] or args["--verbose"]:
            verbose = True

      crearArchivo(lenguage, instalacion)

      sys.exit(0)
  except Exception as e:
    print(e)