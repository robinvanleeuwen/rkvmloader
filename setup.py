from distutils.core import setup

setup(name='rkvmloader',
    version='0.5',
    scripts=["rkvmloader"],
    url="https://github.com/robinvanleeuwen/rkvmloader",
    author="Robin van Leeuwen",
    author_email="robinvanleeuwen@gmail.com",
    install_requires=['libvirt-python==1.3.1',
                      'docopt==0.6.2',
                      'ptyprocess==0.5.1']
)
