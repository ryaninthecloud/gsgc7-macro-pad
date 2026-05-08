'''
Catalogue of response options

Patterns for defining functions to be called
--------------------------------------------
After some thinking, it might be better to do
lambda definitions for things like prints so that
parsing a command can be done somewhat more easily.

x = {'y': lambda a,b: print (a+b)} <-- pattern for prints
Called in interface by x['y']('1','2') --> returns '12'
'''
from os import system

windows_dispatch_catalogue = {
    'D' : {
        '1' : lambda: system('start explorer.exe')
    },
    'H' : lambda a,b: print(a+b)
}

macos_dispatch_catalogue = {

}