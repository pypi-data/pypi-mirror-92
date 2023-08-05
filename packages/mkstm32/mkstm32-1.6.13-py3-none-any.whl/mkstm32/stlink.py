import re
import sys
import time
import readline
import subprocess
import threading

import serial
from serial.tools.list_ports import comports

from .helpers import Option

class STLink:
  '''This class is responsible for ST-Link connection and operations.'''

  def __init__(self, cli):
    self.cli = cli

  @staticmethod
  def devices():
    '''Returns a list of connected devices.'''

    p = subprocess.Popen(['st-info', '--probe'], stdout=subprocess.PIPE)
    data, _ = p.communicate()
    data = data.decode('utf8')

    # Get names of the devices
    name_regex = re.compile(r'descr: (.+)')
    names = name_regex.findall(data)

    # Get serial numbers
    serial_regex = re.compile(r'serial: (.+)')
    serials = serial_regex.findall(data)

    # Zip them together
    devices_ = list(zip(names, serials))

    return devices_

  def list_ports(self):
    '''Lists available serial ports'''
    print('{:4} {:40} {:16} {:16}'.format(
      self.cli.bold('#'),
      self.cli.bold('   Port'),
      self.cli.bold('           Manufacturer'),
      self.cli.bold('    Product')))

    #print('-'*79)
    for i, p in enumerate(comports()):
      print('{:12} {:40} {:16} {:16}'.format(
        self.cli.bold(i),
        str(p.device)[:40],
        str(p.manufacturer),
        str(p.product)))

  def monitor(self, port, baud_rate=9600, uart_reset_time=1):
    '''Starts a serial monitor on a specific port.'''

    def reset_connection(serial_interface):
      self.cli.print('SerialException occurred.', warning=True)
      self.cli.print('Resetting connection...')
      retry_count = 0
      while True:
        retry_count += 1
        self.cli.print('Retry count: {}'.format(retry_count))
        try:
          serial_interface.close()
          time.sleep(uart_reset_time)
          serial_interface.open()
          break
        except serial.SerialException:
          continue

      self.cli.print('Connection reset.')

    def thread_wrapper(func):
      def wrapper(*args, **kwargs):
        try:
          func(*args, **kwargs)
        except UnicodeDecodeError:
          pass
        except UnicodeEncodeError:
          pass
        except KeyboardInterrupt:
          sys.exit()

      return wrapper

    @thread_wrapper
    def keyboard_input(serial_interface):
      while True:
        text = input()
        try:
          serial_interface.write(text.encode() + b'\n')
        except serial.serialutil.SerialException:
          reset_connection(serial_interface)

    @thread_wrapper
    def serial_output(serial_interface):
      while True:
        try:
          sys.stdout.write(serial_interface.read().decode())
        except serial.serialutil.SerialException:
          reset_connection(serial_interface)

    if port is None:
      ports = [Option('{0:40} {1:20}'.format(p.device, p.description), p) for p in comports()]
      port = self.cli.choose(ports).device
      print('Listening on port: {}'.format(port))
      print('  at baud rate {}\n'.format(baud_rate))

    s = None
    try:
      s = serial.Serial(port=port, baudrate=baud_rate)
    except serial.serialutil.SerialException:
      self.cli.print('Serial port failure: {}'.format(port), error=True)

    if s is None:
      sys.exit(1)

    keyboard_input_thread = threading.Thread(
      target=keyboard_input,
      args=[s],
      daemon=True
    )

    serial_output_thread = threading.Thread(
      target=serial_output,
      args=[s],
      daemon=True
    )

    keyboard_input_thread.start()
    serial_output_thread.start()

    try:
      while True:
        pass
    except KeyboardInterrupt:
      sys.exit()

  def probe(self):
    '''Prints detailed information about connected devices.'''

    self.cli.call(['st-info', '--probe'])

  def reset(self):
    '''Resets the MCU.'''

    serial_ = self.cli.choose_serial()
    if serial_ is None:
      self.cli.call(['st-flash', 'reset'])
    else:
      self.cli.call(['st-flash', '--serial', serial_, 'reset'])

