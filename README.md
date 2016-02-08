# rkvmloader
Sequentially load Linux KVM's

   RKVMLoader loads KVM Virtual Machines in a predefined
   sequence. By default domains will initially be
   gracefully shutdown, but forcefully destroyed after a
   timeout (default 30 sec).
   Usage:
       rkvmloader start [-c <file>] [-v]
       rkvmloader stop [-c <file>] [-v] [-t <sec>]
       rkvmloader (-h | --help)
       rkvmloader --version 
   Options: 
     -v --verbose          Be Verbose
     -h --help             Show this screen
     -c --config=<config>  Configuration file [default: /etc/rkvmloader.conf]
     --force               Forcefully kill VM's immidiately
     -t --timeout=<sec>    Force off after <sec> seconds [default: 30]
