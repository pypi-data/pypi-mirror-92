#from . import modulo1
from .modulo1 import print_msg

def suma(x, y):
    #modulo1.print_msg("SUMA")
    print_msg("SUMA")
    return x + y


def resta(x, y):
    #modulo1.print_msg("RESTA")
    print_msg("RESTA")
    return x - y


def producto(x, y):
    #modulo1.print_msg("PRODUCTO")
    print_msg("PRODUCTO")
    return x*y


def division(x, y):
    #modulo1.print_msg("DIVISION")
    print_msg("DIVISION")
    return x/y


def info():
    print("suma, resta, producto, division")