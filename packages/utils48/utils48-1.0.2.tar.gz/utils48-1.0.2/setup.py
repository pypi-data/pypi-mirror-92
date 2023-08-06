from distutils.core import setup
import sys
version=sys.argv.pop()
setup(
  name = 'utils48',         # How you named your package folder (MyLib)
  packages = ['utils48'],   # Chose the same as "name"
  version = version,      # Start with a small number and increase it with every change you make
  description = 'some utilities',   # Give a short description about your library
  author = '48panda',                   # Type in your name
  url = 'https://github.com/48panda48/48util',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/48panda48/48util/archive/'+version+'.tar.gz',    # I explain this later on
  )
