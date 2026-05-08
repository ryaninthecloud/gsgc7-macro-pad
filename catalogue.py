'''
Catalogue of response options

D = Dial --> needs to search for the integers dialled

dispatch catalogue:
strings:
    if begin with < then sent to serial device
    if begin with ! then printed to console
    if begin with # then are commands sent to pc
    
Patterns for defining functions to be called
--------------------------------------------
After some thinking, it might be better to do
lambda definitions for things like prints so that
parsing a command can be done somewhat more easily.

x = {'y': lambda a,b: print (a+b)} <-- pattern for prints
Called in interface by x['y']('1','2') --> returns '12'
'''

def my_command():
    print('hello! from the catalogue!')

windows_dispatch_catalogue = {
    'D' : {
        '1' : '!Someone is calling us!'
    },
    'H' : lambda a,b: print(a+b)
}

macos_dispatch_catalogue = {

}