#!/usr/bin/python

import json
import subprocess
import sys
from pprint import pprint

proc = subprocess.Popen(['vtysh', '-c', 'show bgp neighbors json'], stdout=subprocess.PIPE)
data = proc.stdout.read()

bgp_neighbors = json.loads(data)
failed=False

for neighbor in bgp_neighbors:
  if neighbor != "bestPath":
    ipv4_prefixes = bgp_neighbors[neighbor]['addressFamilyInfo']['IPv4 Unicast']['acceptedPrefixCounter']
    if ipv4_prefixes == 0:
      failed=True
    print("neigbor: %s, v4 prefixes %s" % (neighbor, ipv4_prefixes))


if failed:
  sys-exit(1)
