# rkvmloader
Sequentially load Linux KVM's

Rkvmloader checks the KVM XML definition for all MAC addresses of interface cards, boots the 
virtual machine and checks the local ARP cache table to see if an interface comes up at one
of these MAC addresses. It waits for s successfull network connection on this IP address to a
given port (connect to port 22 for exmaple) or continues booting the next VM in the list.

```
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
```

See rkvmloader.conf for a configration example and documentation
