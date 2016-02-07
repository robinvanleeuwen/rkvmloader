#!/usr/bin/env python3
"""RKVMLoader

RKVMLoader loads KVM Virtual Machines in a predefined
sequence. By default domains will be gracefully shutdown.

Usage:
    rkvmloader.py start [-c <file>] [-v]
    rkvmloader.py stop [-c <file>] [-v]
    rkvmloader.py (-h | --help)
    rkvmloader.py --version

Options:
  -v --verbose          Be Verbose
  -h --help             Show this screen
  -c --config=<config>  Configuration file [default: /etc/rkvmloader.conf]
  --force               Forcefully kill VM's
"""
import socket
import subprocess

import docopt
import configparser
import libvirt
import sys
import xml.etree.ElementTree as ET
import time

qemu_host = 'qemu:///system'

def print_v(message, *args, **kwargs):
    if arguments['--verbose']: print(message, *args, **kwargs)


def qemu_connect():
    print_v("(I) Connecting to %s" % qemu_host)

    conn = libvirt.open(qemu_host)

    if conn is None:
        print('(E) Failed to connect to qemu:///system', file=sys.stderr)
        exit(1)

    return conn


def load_config_file(configfile):
    error = False
    conf = configparser.ConfigParser()
    conf.read(configfile)

    try:
        hosts = conf['hosts']['sequence'].split(',')
    except KeyError:
        print("(E) %s: Couldn not find 'sequence' in section [hosts]." % configfile)
        sys.exit(1)

    for h in hosts:
        if h not in conf:
            print("(E) %s: Could not find declaration of host '%s'" % (configfile, h))
            error = True

    if error:
        sys.exit(1)

    return conf


def determine_host_macs(conn, host_name):
    mac_list = []
    print_v("(I) Detrmining MAC's for %s " % host_name, end="")
    vm_xml = conn.lookupByName(host_name).XMLDesc()
    root = ET.fromstring(vm_xml)
    for i in root.findall('./devices/interface'):
        for mac in i.findall('mac'):
            mac_list.append(mac.attrib['address'])
    print_v("found %s" % mac_list)
    return mac_list


def start_vm(conn, host_name):

    waitfor = config[host_name]['waitfor'].split(':')
    up = False
    if host_name in [conn.lookupByID(x).name() for x in conn.listDomainsID()]:
        print_v('(I) Host %s already running' % host_name)
    else:
        print_v("(I) Starting %s " % (host_name,))
        conn.lookupByName(host_name).create()
        mac_list = determine_host_macs(conn, host_name)
        print_v("(I) Waiting for ARP cache to be filled... ", end="")
        sys.stdout.flush()
        while not up:

            for mac in mac_list:
                cmd = "arp -n | grep %s | awk ' { print $1 }'" % mac
                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                output, errors = p.communicate()
                if output != b'':
                    ip = output.decode('UTF-8').strip('\n')
                    print("Found %s" % ip)
                    up = True
            time.sleep(1)

        print_v("(I) Checking %s port %s on %s... " % (waitfor[0], waitfor[1], ip), end="")
        sys.stdout.flush()

        connected = False
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        while not connected:
            if sock.connect_ex((ip, int(waitfor[1]))) != 0:
                time.sleep(1)
            else:
                connected = True
                print_v('Connection succeeded.', end="\n")

        print_v("Done booting %s" % host_name)



if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version="RKVMLoader 0.1")
    config = load_config_file(arguments['--config'])
    conn = qemu_connect()
    rvmids = conn.listDomainsID()
    print_v("(I) Running VM id's: %s" % rvmids)

    if arguments['start']:
        sequence = config['hosts']['sequence'].split(',')
        print_v("(I) Starting VM's in sequence %s" % sequence)
        for host in sequence:
            sucess = start_vm(conn, host)

    if arguments['stop']:
        sequence = [ x for x in reversed(config['hosts']['sequence'].split(','))]
        print_v("(I) Stopping VM's in sequence %s" % sequence)
        for host in sequence:
            if host not in [conn.lookupByID(x).name() for x in rvmids]:
                print_v('(I) Host %s already stopped' % host)
            else:
                print_v('(I) Stopping %s' % host)
