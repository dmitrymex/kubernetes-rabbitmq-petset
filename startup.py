#!/usr/bin/python

import os
import re
import socket
import subprocess
import sys
import time


def execute(cmd):
    return subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr)


def check_execute(cmd):
    return subprocess.check_call(cmd, stdout=sys.stdout, stderr=sys.stderr)


def init_and_start_rabbit(our_fqdn):
    with open('/etc/rabbitmq/rabbitmq-env.conf', 'a') as env_conf:
        env_conf.write('USE_LONGNAME=true\n')
        env_conf.write('NODENAME=rabbit@%s\n' % our_fqdn)

    return subprocess.Popen(['rabbitmq-server'], stdout=sys.stdout, stderr=sys.stderr)


def wait_cluster_status_ok():
    while execute(['rabbitmqctl', 'cluster_status']) != 0:
        time.sleep(1)


def signal_readiness():
    with open('/tmp/rabbit_ready', 'w'):
        pass


def join_leader(leader_fqdn):
    check_execute(['rabbitmqctl', 'stop_app'])
    check_execute(['rabbitmqctl', 'join_cluster', 'rabbit@%s' % leader_fqdn])
    check_execute(['rabbitmqctl', 'start_app'])


our_fqdn = socket.getfqdn()

proc = init_and_start_rabbit(our_fqdn)

if re.match('^([a-zA-Z0-9-]*)-0(\\.|$)', our_fqdn):
    # We are the first node
    wait_cluster_status_ok()
    signal_readiness()

else:
    # We are a following node and need to join to the first node
    # But first signal readiness immediately so that other followers could start
    signal_readiness()
    wait_cluster_status_ok()

    leader_fqdn = re.sub('^([a-zA-Z0-9-]*)-[0-9]+(\\.|$)', '\\1-0\\2', our_fqdn)
    join_leader(leader_fqdn)

exit(proc.wait())
