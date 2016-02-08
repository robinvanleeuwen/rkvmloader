# rkvmloader
Sequentially load Linux KVM's
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

The configuration file should be defined as follows:

```
# RKVMLoader configuration file.
# The default location is /etc/rkvmloader.py, but the -c option can
# choose another file.


# The file needs a [hosts] section wit a sequence variable to
# describe in which sequence the VM's should be started. The
# reverse order will be used for stopping the VM's
# the sequence variable describes the host-names as defined in
# libvirt XML files of that host.

# Example:
[hosts]
sequence = vm1,win1

# Every VM described in the sequence shoud have a section
# In this section the waitfor-variable tells rkvmloader to
# wait for a certain network occurence. PASS can be used
# to just wait for the local network to come up.

# Example: Wait for TCP port 22 to come up
[vm1]
waitfor = TCP:22

# Example: Only wait for the network interface to come up
# and receive an IP:
[win1]
waitfor = PASS

```
