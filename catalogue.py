'''
Catalogue of response options

D = Dial --> needs to search for the integers dialled

dispatch catalogue:
strings:
    if begin with < then sent to serial device
    if begin with ! then printed to console
    if begin with # then are commands sent to pc
    

'''

def my_command():
    print('hello! from the catalogue!')

windows_dispatch_catalogue = {
    'D' : {
        '1' : '!Someone is calling us!'
    },
    'H' : my_command
}

macos_dispatch_catalogue = {

}