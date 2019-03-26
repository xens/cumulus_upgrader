#!/usr/bin/python

import json
import subprocess
import sys

proc = subprocess.Popen(['/usr/bin/clagctl', '-j'], stdout=subprocess.PIPE)
data = json.loads(proc.stdout.read())

if 'errorMsg' in data:
    sys.exit(0)

clagIntfs = data['clagIntfs']
clagStatus = data['status']
failed = False

print(
    '# HELP clag_interfaces_count (0=absent on both peers, 1=single connected, 2=dual connected)'
)
print('# TYPE clag_interfaces_count gauge')

for port in clagIntfs:
    if clagIntfs[port]['status'] == "single":
        value = 1
        failed = 1
    elif clagIntfs[port]['status'] == "dual":
        value = 2
    else:
        failed = 1
        value = 0

    print('clag_interface_count{name="%s"} %s' % (port, value))

print('# HELP clag_peer_status (0=Peer absent, 1=Peer connected)')
print('# TYPE clag_peer_status gauge')

if clagStatus['peerAlive']:
    value = 1
else:
    failed = 1
    value = 0

print('clag_peer_status %s' % value)

print('# HELP clag_peer_backup_active')
print('# TYPE clag_peer_backup_active gauge')
print('clag_peer_backup_active %s' % (clagStatus['backupActive'] and 1 or 0))

print('# HELP clag_peer_our_role (1=primary, 2=secondary)')
print('# TYPE clag_peer_our_role gauge')
print(
    'clag_peer_our_role %s' % (clagStatus['ourRole'] == 'primary' and 1 or 2)
)

print('# HELP clag_peer_peer_role (1=primary, 2=secondary)')
print('# TYPE clag_peer_peer_role gauge')
print(
    'clag_peer_peer_role %s' %
    (clagStatus['peerRole'] == 'primary' and 1 or 2)
)

if failed:
  sys-exit(1)
