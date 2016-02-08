from distutils.core import setup

setup(name = 'rkvmloader',
      version = '0.1',
      scripts = ["rkvmloader"],
      py_modules = ["docopt", "configparser", "libvirt"],
      url = "https://github.com/robinvanleeuwen/rkvmloader",
      author = "Robin van Leeuwen",
      author_email = "robinvanleeuwen@gmail.com"
)