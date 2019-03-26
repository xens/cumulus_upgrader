#!/usr/bin/python

import json
import subprocess

def ptm():
    ptmctl = subprocess.Popen(['ptmctl', '-j'], stdout=subprocess.PIPE)
    return json.loads(ptmctl.stdout.read())


def test_cbl(ptm):
    cbl = {}
    for key, value in ptm.items():
        cbl[value['port']] = (value['cbl status'] == 'pass')
    failed = [port for port, state in cbl.items() if not state]
    assert not failed, \
        'CBL failed on the following ports: %s' % ', '.join(failed)

def test_bfd(ptm):
    bfd = {}
    for key, value in ptm.items():
        status = value['BFD status']
        port = value['port']

        if status == 'pass':
            bfd[port] = True
        elif status == 'N/A':
            bfd[port] = None
        else:
            bfd[port] = False

    failed = [port for port, state in bfd.items() if state is False]
    assert not failed, \
        'BFD failed on the following ports: %s' % ', '.join(failed)

if __name__ == '__main__':

    topology = ptm()
    cbl_status = test_cbl(topology)
    bfd_status = test_bfd(topology)
