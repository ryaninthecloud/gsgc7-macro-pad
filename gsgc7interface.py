'''
The agent that runs and
interprets the messages from
the GSGC7 unit and fires
the relevant automation.

TODO: MacOS port
'''

from serial import (
    Serial,
    SerialTimeoutException,
    SerialException
)

import time

class GSGC7Interface:
    def __init__(self, com_port: str):
        '''
        Args:
            com_port (str): the comm port that is connected to GSGC7
        '''
        self.com_port = com_port
        self.serial_cx = self.__create_connection()
        self.control_characters = ['\n', '\r', '\r\n']
        time.sleep(2)

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

    def __parse_instruction(self, raw_command: bytes) -> str | None:
        '''
        Consumes a given byte string and returns
        only the instructive portion of the AT
        command/message

        Args:
            raw_command (bytes): received from the GSGC7 device

        Returns:
            cleaned_command (str): cleaned non-AT portion of command
        '''
        try:
            decoded_raw_command = raw_command.decode(encoding='utf-8')
            decoded_raw_command = decoded_raw_command.upper().strip()
        except UnicodeDecodeError:
            print('Unable to decode the given command')
            return None

        if decoded_raw_command in self.control_characters:
            print('Something here to flush the cache')
            return None

        if not decoded_raw_command or \
        len(decoded_raw_command) <= 2 or \
        decoded_raw_command[:2] not in ('AT', '<'):
            print('Command invalid and not parsed: ', decoded_raw_command)
            return None

        if decoded_raw_command[0] == '<':
            print('Interpreter message received: ', decoded_raw_command)
            return None

        instructive_portion = decoded_raw_command[2:]

        return instructive_portion

    def send_ringtone(self) -> bool:
        '''
        Sends a ring command to the GSGC7 which
        sounds a bleep and illuminates the red
        ISDN Line light for a short period.

        Returns:
            result (bool)
        '''
        return self.__send_instruction('RING')

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

if __name__ == "__main__":
    g = GSGC7Interface('COM5')