from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'animaty',         
  packages = ['animaty'],   
  version = '0.1',      
  license='MIT',        
  description = 'animaty is a library for animating ascii art in python.', 
  long_description = long_description,
  long_description_content_type = 'text/markdown',  
  author = 'Vincent Elias Mallon',      
  url = 'https://github.com/GaiaHacking',
  download_url= 'https://github.com/GaiaHacking/animaty/archive/0.1.tar.gz',
  keywords = ['ASCII', 'Animation', 'Console', 'Terminal'],   
  install_requires=['windows-curses; sys_platform == "win32"'],
)