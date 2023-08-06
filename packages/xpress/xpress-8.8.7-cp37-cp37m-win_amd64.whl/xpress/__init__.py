import os
import os.path
import sys
import platform

oldcwd = os.getcwd()

os.chdir (os.path.dirname (os.path.realpath(__file__)))

base_path = os.path.dirname (os.path.realpath(__file__))
libpath = base_path + '/lib'

if platform.system() == 'Windows':
  os.environ['PATH'] = libpath + ';' + libpath + '../../../;' + os.environ['PATH']

def manual():
  """
  Print an informative message about where to find the PDF reference
  manual of the Python interface and the URL of the on-line
  documentation for all of the Xpress-related software tools.

  Syntax: xpress.manual()

  Note that only the manual of the Python interface (in PDF format) is
  included in the PyPI and conda package downloaded from these
  repositories; the PDF version of all other Xpress-related
  documentation is contained in the Xpress distribution, and the
  on-line, HTML format documentation is available on the FICO web pages.
  """

  # The following commands have the same output on Python 2 and 3 and
  # don't require importing print_function from __future__
  print("Please find the manual for the Xpress Python Interface in your installation at\n\n" +
        base_path + "/xpress/doc/python-interface.pdf" + '\n')
  print("The online documentation includes that for the Xpress Optimizer and the Nonlinear solvers\n"
        "and can be found at https://www.fico.com/fico-xpress-optimization/docs/latest/overview.html")

try:
  from xpresslib import *
except:
  print('Could not import xpress module.\n\
If you have a full installation of the FICO-Xpress suite version 8.5.2 or earlier,\n\
you should delete all files named xpress*.pyd in the c:\\xpressmp\\bin directory and\n\
subdirectories (this may vary depending on where the FICO-Xpress installation is\n\
located). On Linux or MacOS systems, delete all files named xpress*.so in /opt/xpressmp/lib.')
  raise

if 'XPRESS' not in os.environ.keys():
  os.environ['XPRESS'] = os.path.dirname (os.path.realpath(__file__)) + '/license'
  print("Using the Community license in this session. If you have a full Xpress license,\n\
first set the XPRESS environment variable to the directory containing the license file,\n\
xpauth.xpr, and then restart Python. If you want to use the FICO Community license\n\
and no longer want to see this message, set the XPRESS environment variable to\n", os.environ['XPRESS'])

os.chdir (oldcwd)

del libpath
del oldcwd
del os
del sys
del platform
