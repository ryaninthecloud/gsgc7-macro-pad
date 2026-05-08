'''
The agent that runs and
interprets the messages from
the GSGC7 unit and fires
the relevant automation.

TODO: MacOS port
TODO: Detect OS & call catalogue reader

'''

from serial import (
    Serial,
    SerialTimeoutException,
    SerialException
)
from typing import (
    Callable
)

import time

class GSGC7Interface:
    def __init__(self, com_port: str):
        '''
        Args:
            com_port (str): the comm port that is connected to GSGC7
        '''
        self.dispatch_catalogue = None
        self.com_port = com_port
        self.serial_cx = self.__create_connection()
        self.control_characters = ['\n', '\r', '\r\n']
        self.__read_catalogue('windows')

    def __create_connection(self) -> Serial:
        '''
        Creates connection to the device

        Args:
            None
        Returns:
            _ (Serial): COM port connection to the GSGC7 Device
        '''
        try:
            print(self.com_port)
            _ = Serial(self.com_port, 9600, timeout=0, bytesize=8)
            return _
        except SerialTimeoutException:
            print('Could not connect to given COM port. Exiting...')
            exit(0)
        except SerialException as ser_exc:
            print('A Serial Exception has occured when connecting to given COM port: ', ser_exc)
            exit(0)
        except Exception as excpt:
            print('An unexpected error has occured when connecting to the given COM port: ', excpt)
            exit(0)

    def __parse_instruction(self, raw_command: str) -> str | None:
        '''
        Consumes a given byte string and returns
        only the instructive portion of the AT
        command/message

        Args:
            raw_command (bytes): received from the GSGC7 device

        Returns:
            cleaned_command (str): cleaned non-AT portion of command
        '''
        stdised_command = raw_command.upper().strip()

        if not stdised_command or \
        len(stdised_command) <= 2 or \
        stdised_command[:2] not in ('AT', '<'):
            print('Command invalid and not parsed: ', stdised_command)
            return None

        if stdised_command[0] == '<':
            print('Interpreter message received: ', stdised_command)
            return None

        instructive_portion = stdised_command[2:]

        return instructive_portion

    def __send_instruction(self, instruction: str) -> bool:
        '''
        For communicating with the GSGC7 device -- this
        code contains at a maximum 2.5 seconds of processing
        time that allows the GSGC7 to read and interpret
        an instruction.

        Args:
            instruction (str): instruction to be sent in entirety

        Returns:
            result (bool): success true, failure false
        '''
        if not self.serial_cx.is_open:
            print('Could not communicate with device, serial cx not open')
            return False

        try:
            instruction += '\r\n'
            encoded_instruction = instruction.encode()
        except UnicodeEncodeError:
            print('Could not encode instruction')
            return False

        delivered = False
        retry_attempt = 0

        while not delivered and retry_attempt < 3:
            if self.serial_cx.writable():
                delivered = True
                self.serial_cx.write(encoded_instruction)
            else:
                time.sleep(0.5)
                retry_attempt += 1

        time.sleep(1)
        print('Delivery failed within alloted tries.') if not delivered else None
        return delivered

    def __read_catalogue(self, os_type: str) ->  None:
        '''
        Read from the catalogue file in same directory

        Args:
            os_type (str): [windows, macos]

        Returns:
            None
        '''
        try:
            if os_type.lower() == 'windows':
                from catalogue import windows_dispatch_catalogue
                self.dispatch_catalogue = windows_dispatch_catalogue
            elif os_type.lower() == 'macos':
                from catalogue import macos_dispatch_catalogue
                self.dispatch_catalogue = macos_dispatch_catalogue
        except ModuleNotFoundError:
            print('Cannot find catalogue module')
            exit(0)

        return None
        
    def send_ringtone(self) -> bool:
        '''
        Sends a ring command to the GSGC7 which
        sounds a bleep and illuminates the red
        ISDN Line light for a short period.

        Returns:
            result (bool)
        '''
        return self.__send_instruction('RING')

    def send_no_carrier(self) -> bool:
        '''
        Look, we work with what we have and I think
        that NO CARRIER might be the best approach to
        a positive status message to close the cx once
        a command is dialed in to the pad
        
        Returns:
            result (bool)
        '''
        return self.__send_instruction('NO CARRIER')

    def send_connect(self) -> bool:
        '''
        Sends a CONNECT to GCGC7 - this will need to be
        followed by a FRAMED command to complete the connection.

        Returns:
            result (bool)
        '''
        return self.__send_instruction('CONNECT')

    def handle_incoming_instruction(self, raw_command: str) -> None:
        '''
        Reads the catalogue of automations
        and calls the correct dispatcher
        for the instruction

        Args:
            raw_instr (bytes): a raw message/AT command

        Returns:
            None
        '''
        if not self.dispatch_catalogue:
            exit(0)

        cleaned_instruction = self.__parse_instruction(raw_command)

        if not cleaned_instruction:
            return None

        if cleaned_instruction[0] not in self.dispatch_catalogue.keys():
            return None

        if cleaned_instruction[0] == 'H':
            self.dispatch_catalogue['H']('yummy', 'delicious')

        if cleaned_instruction[0] == 'D':
            if len(cleaned_instruction) < 2:
                return None
            if cleaned_instruction[1:] not in self.dispatch_catalogue['D']:
                return None
            else:
                cat_val = self.dispatch_catalogue['D'][cleaned_instruction[1:]]
                if not isinstance(cat_val, Callable):
                    return None
                else:
                    cat_val()
        return None

                
        

    def start_listening(self):
        '''
        Start listening to the comm port
        for messages.
        '''
        def handle_byte(b) -> str:
            try:
                decoded_data = raw_data.decode(encoding='utf-8')
            except UnicodeDecodeError:
                decoded_data = 'x?x'
            return decoded_data

        current_command = ''

        while self.serial_cx.is_open:
            raw_data = self.serial_cx.read()
            if raw_data:
                decoded_data = handle_byte(raw_data)
                if decoded_data not in self.control_characters:
                    current_command += decoded_data
                else:
                    if current_command:
                        self.handle_incoming_instruction(current_command)
                        current_command = ''

if __name__ == "__main__":
    g = GSGC7Interface('COM5')
    g.start_listening()