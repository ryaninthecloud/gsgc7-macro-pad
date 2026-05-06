import serial
import time

from types import FunctionType

from catalogue import dispatch_catalogue

def dispatch(f: FunctionType | str | list):
    '''
    dispatch takes arguments from the
    dispatch catalogue and does stuff
    with them
    '''


def decipher_message(message: str) -> None:
    '''
    decodes the AT command and performs/calls
    an action based on the type and content.
    '''
    message = message.strip().upper()

    if message[:2] in ['<']:
        if 'NOACK' in message:
            return None
        else:
            print('[WARN]: SYSTEM MESSAGE: ', message)
            return None

    if message[:2] != 'AT':
        return None

    message = message[2:]
    print(f'Message is {message}')

    '''if message[0] not in dispatch_catalogue:
        return None
    else:
        tier_1_function = dispatch_catalogue[message[0]]
        if type(tier_1_function, str):'''
            

ser = serial.Serial('COM5', 9600, timeout=0, bytesize=8)
command = ''
control_characters = ['\n', '\r', '\r\n']

while ser.is_open:
    raw_data = ser.read()
    if raw_data:
        try:
            decoded_data = raw_data.decode(encoding='utf-8')
        except UnicodeDecodeError:
            decoded_data = 'x?x'
        if decoded_data not in control_characters:
            command += decoded_data
        else:
            if command:
                print('decipher', command)
                decipher_message(command)
                command = ''