import os
import sys
import time
import shutil
import subprocess

from .helpers import Option
from .stlink import STLink
from .config import Config

class Project:
  '''This class is responsible for handling an STM32CubeMX project.'''

  def __init__(self, dir_, cli, stlink, cpp=False):
    self.cli = cli
    self.stlink = stlink

    self.dir = os.path.abspath(dir_)
    self.cpp = cpp

    self.start = None

    os.chdir(self.dir)

  # __enter__ and __exit__ make possible to measure time
  # using `with` statement
  def __enter__(self):
    self.start = time.time()
    return self

  def __exit__(self, ex_type, ex_val, traceback):
    took = time.time() - self.start
    if took > 0.05:
      self.cli.print(
        'Done in {0:0.2f} seconds.'.format(time.time() - self.start),
        verbosity=2)

  def executable(self, ext='.bin'):
    '''Adds an extension to compiled executables based on
    the project's name.'''

    return self.path(os.path.join(Config.build_dir,
                     os.path.basename(self.dir) + ext))

  def path(self, file_=''):
    '''Returns path relative to the project directory.'''

    return os.path.join(self.dir, file_)

  def make(self):
    '''Calls make and creates makefile for C++ if needed.'''

    success_msg = 'Successfuly compiled firmware'
    if self.cpp:
      self.cli.print('Compiling for C++', verbosity=1)
      self.generate_cpp_makefile()
      self.cli.call([
              'make',
              '-j', '4',
              '-f', self.path(Config.cpp_makefile)
          ], success_message=success_msg)
    else:
      self.cli.print('Compiling for C', verbosity=1)
      self.cli.call([
          'make',
          '-j', '4',
          '-f', self.path(Config.standard_makefile)
      ], success_message=success_msg)

  def generate_cpp_makefile(self):
    '''Converts standard Makefile to C++ Makefile.'''

    with open(self.path(Config.standard_makefile), 'r') as f:
      data = f.read()

    data = data.replace('gcc', 'g++')
    splitdata = data.splitlines()

    for i, line in enumerate(splitdata):
      if 'LDFLAGS =' in line:
        splitdata.insert(i+1, 'LDFLAGS += -specs=nosys.specs')

      if 'CFLAGS =' in line:
        splitdata.insert(i+1, 'CFLAGS += -std=c++17 -Wno-register')

    with open(self.path(Config.cpp_makefile), 'w') as f:
      f.write('\n'.join(splitdata))

  def upload(self, method='stlink'):
    '''Uploads the project to the microcontroller.'''

    if method == 'stlink':
      serial_ = self.cli.choose_serial()
      if serial_ is None:
        self.cli.call(
          ['st-flash', 'write', self.executable(), Config.flash_address],
          success_message='Successfully uploaded firmware.')
      else:
        self.cli.call(['st-flash',
                      '--serial', serial_,
                      'write', self.executable(), Config.flash_address],
                      success_message='Successfully uploaded firmware.')
    elif method == 'dfu':
      self.cli.call(['dfu-util',
        '-d', '0483:df11',
        '-a', '0',
        '-s', '{}:leave:force:{}'.format(
          Config.flash_address, self.size()['.bin']),
        '-D', self.executable()],
        success_message='Successfully uploaded firmware.')

  def debug(self):
    '''Starts a GDB server and calls arm-none-eabi-gdb debugger.'''

    serial_ = self.cli.choose_serial()
    if serial_ is None:
      self.cli.print('Starting GDB server.', verbosity=1)
    else:
      self.cli.choose([Option('{0:20} {1:40}'.format(device[0],
                      device[1]), device) for device in STLink.devices()])

    kwargs = {}
    if self.cli.verbosity < 3:
      kwargs = {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}

    gdb_server = subprocess.Popen(['st-util'], **kwargs)

    time.sleep(0.1)
    if gdb_server.poll():
      self.cli.print('Failed to start GDB server.', error=True)
    else:
      self.cli.print('Successfully started GDB server.', verbosity=2)

    try:
      self.cli.call(['arm-none-eabi-gdb', self.executable('.elf'),
                    '-ex', 'tar extended-remote :4242'])
    except KeyboardInterrupt:
      pass
    finally:
      self.cli.print('Closing GDB server.', verbosity=1)
      gdb_server.kill()
      self.cli.print('GDB server killed.', verbosity=2)

  def size(self):
    '''Prints size of the compiled binaries.'''

    out = {}
    for ext in ['.bin', '.elf', '.hex']:
      file_ = self.executable(ext)
      try:
        with open(file_, 'r') as f:
          f.seek(0, 2)
          size_ = f.tell()
          self.cli.print('{}: {} B'.format(os.path.basename(file_), size_))
          out[ext] = size_
      except FileNotFoundError:
        self.cli.print('File not found.', error=True)
        sys.exit(1)

    return out

  def clean(self):
    '''Cleans the build directory.'''

    self.cli.print('Cleaning build directory.', verbosity=1)

    try:
      shutil.rmtree(Config.build_dir)
      self.cli.print('Successfully cleaned build directory.', verbosity=2, success=True)
    except FileNotFoundError:
      self.cli.print('Build directory doesn\'t exist.', error=True)

