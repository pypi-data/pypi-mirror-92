import os
import readline
import sys
import subprocess

from .helpers import Option
from .stlink import STLink

def formatter(func):
  '''Checks for ANSI escape codes support.
  Those are responsible for colorful messages.'''

  def wrapper(text):
    posix_support = os.name == 'posix' and hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    win_support = os.name == 'nt' and 'ANSICON' in os.environ
    if posix_support or win_support:
      return func(text)
    return text

  return wrapper

class CLI:
  '''This class is responsible for I/O interaction with the user'''

  def __init__(self, progname, verbosity=0):
    self.verbosity = verbosity

    # Program name prepended to every printed message
    self.footprint = CLI.bold(os.path.basename(progname)) + ':'

  @staticmethod
  @formatter
  def bold(text):
    return '{}{}{}'.format('\033[1m', text, '\033[0m')

  @staticmethod
  @formatter
  def red(text):
    return '{}{}{}'.format('\033[31m', text, '\033[0m')

  @staticmethod
  @formatter
  def green(text):
    return '{}{}{}'.format('\033[32m', text, '\033[0m')
  
  @staticmethod
  @formatter
  def yellow(text):
    return '{}{}{}'.format('\033[33m', text, '\033[0m')

  def choose(self, options, title='Choose one of the following:'):
    ''' Prompts user to choose one of available options'''

    self.print(title)

    for i, o in enumerate(options):
      self.print('[{}] {}'.format(i, o.key))

    try:
      choice = int(input('> '))
      return options[choice].value
    except IndexError:
      self.print('No valid option chosen.', error=True)
      sys.exit(1)
    except ValueError:
      self.print('No valid option chosen.', error=True)
      sys.exit(1)
    except KeyboardInterrupt:
      sys.exit()

  def choose_serial(self):
    '''Prompts user to choose a certain device when there's
    many of them.'''

    devices = [Option('{0:20} {1:40}'.format(device[0],
              device[1]), device) for device in STLink.devices()]

    if not devices:
      self.print('Could not find any ST-Link devices.', error=True)
      sys.exit(1)

    if len(devices) > 1:
      serial_ = self.choose(devices)[1]
      return serial_
    return None

  def print(self, text, verbosity=0, success=False, error=False, warning=False):
    '''Prints messages to stdout taking into account things like verbosity, etc.'''

    if self.verbosity < verbosity:
      return

    if error:
      sys.stderr.write('{} {}\n'.format(self.footprint, CLI.bold(CLI.red(text))))
    elif success:
      print(self.footprint, CLI.bold(CLI.green(text)))
    elif warning:
      print(self.footprint, CLI.bold(CLI.yellow(text)))
    else:
      print(self.footprint, text)

  def call(self, arglist, exit_on_error=True, success_message=None):
    '''Calls another programs and handles errors.'''

    kwargs = {}
    if self.verbosity < 1:
      kwargs = {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}

    try:
      if subprocess.call(arglist, **kwargs):
        self.print('Failure while executing {}.\n'.format(arglist[0]), error=True)
        if exit_on_error:
          sys.exit(1)
      elif success_message is not None:
        self.print(success_message, success=True, verbosity=2)
    except FileNotFoundError:
      self.print('Command not found: {}.'.format(arglist[0]), error=True)
      self.print('Make sure you\'ve included all the necessary executables in your PATH.')
      self.print('See README.md for more information.')
      sys.exit(1)
    except KeyboardInterrupt:
      self.print('{} interrupted.'.format(arglist[0]), error=True)
      sys.exit(1)

